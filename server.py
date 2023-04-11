from flask import Flask,render_template,request, redirect, url_for
from SPARQLWrapper import SPARQLWrapper, JSON
from saved_queries import saved_queries
from flask import jsonify
import json
import urllib.parse
from config import *




sparql_ontology = SPARQLWrapper(ENDPOINT_ONTOLOGY)
sparql_resources = SPARQLWrapper(ENDPOINT_RESOURCES)
sparql_history = SPARQLWrapper(ENDPOINT_HISTORY)


list_classes_destaque = []
query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix optq: <http://eu.optique.ontology/annotations#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    select ?class where {
        ?class optq:tem_destaque "true"^^xsd:boolean
    }
"""
sparql_ontology.setQuery(query)
# print(query)
sparql_ontology.setReturnFormat(JSON)
results = sparql_ontology.query().convert()
propriedades = {}
for result in results["results"]["bindings"]:
    list_classes_destaque.append(result['class']['value'])

if len(list_classes_destaque) == 0:
    list_classes_destaque = ['http://xmlns.com/foaf/0.1/Organization','http://www.sefaz.ma.gov.br/ontology/Estabelecimento','http://www.sefaz.ma.gov.br/ontology/Fornecedor','http://xmlns.com/foaf/0.1/Person','http://www.sefaz.ma.gov.br/ontology/Produto']

app = Flask(__name__)

@app.route("/")
def index():    
    return render_template("index.html")

@app.route("/resources/<page>/")
def resources(page,methods=['GET']):
    search = request.args.get('search',default="")
    classRDF = request.args.get('classRDF',default="")
    label = request.args.get('label',default="Busca")
    return render_template("resources.html",page=page,search=search,classRDF=classRDF,label=label)


@app.route("/classes")
def classes():
    query = """
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?class ?label (GROUP_CONCAT(?c;separator=".\\n") as ?comment) where { 
            {
                ?class a owl:Class.
            }
            UNION{
                ?class a rdfs:Class.
            }
            OPTIONAL{
                ?class rdfs:label ?l.
            
            }
    		OPTIONAL{
                ?class rdfs:comment ?c.
            }
            BIND(COALESCE(?l,?class) AS ?label)
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2000/01/rdf-schema#"))
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2001/XMLSchema#"))
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2002/07/owl#"))
        }GROUP BY ?class ?label
        ORDER BY ?label  
		     
    """
    sparql_ontology.setQuery(query)
    # print(query)
    sparql_ontology.setReturnFormat(JSON)
    results = sparql_ontology.query().convert()
    classes = []
    classes_destaque = []
    for result in results["results"]["bindings"]:
        query = f"""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?sub ?label where {{ 
                ?sub rdfs:subClassOf <{result['class']['value']}>.
                OPTIONAL{{
                    ?sub rdfs:label ?l.
                
                }}
                BIND(COALESCE(?l,?sub) AS ?label)
            }}
            ORDER BY ?label  
        """
        subclasses = []
        sparql_ontology.setQuery(query)
        # print(query)
        sparql_ontology.setReturnFormat(JSON)
        results_subclass = sparql_ontology.query().convert()
        for result_subclass in results_subclass["results"]["bindings"]:
            uri = result_subclass['sub']['value']
            label = result_subclass['label']['value']
            if 'http' in label:
                label = label.split("/")[-1].split("#")[-1]
            subclasses.append([uri,label])
        class_ = {'uri':urllib.parse.quote(result['class']['value']),'uri_raw':result['class']['value'],'label':result['label']['value'],'comment':result['comment']['value'],'subclasses':subclasses}
        if "http" in class_['label']:
            class_['label'] = class_['label'].split("/")[-1].split("#")[-1]
        classes.append(class_)
        if result['class']['value'] in list_classes_destaque:
            classes_destaque.append(class_)
    return json.dumps({'classes':classes,'classes_destaque':classes_destaque}, ensure_ascii=False).encode('utf8')

@app.route("/propriedades")
def propriedades():
    query = """
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?property ?label where { 
            {
                ?property a owl:ObjectProperty.
            }
    		UNION{
                ?property a owl:DatatypeProperty.
            }
            UNION{
                ?property a rdfs:Property.
            }
            OPTIONAL{
                ?property rdfs:label ?l
            
            }
            BIND(COALESCE(?l,?property) AS ?label)
        }
        ORDER BY ?label  
    """
    sparql_ontology.setQuery(query)
    # print(query)
    sparql_ontology.setReturnFormat(JSON)
    results = sparql_ontology.query().convert()
    propriedades = {}
    for result in results["results"]["bindings"]:
            
        label = result['label']['value']
        if "http" in label:
            label = label.split("/")[-1].split("#")[-1]
        propriedades[result['property']['value']] = label

    return json.dumps({'propriedades':propriedades}, ensure_ascii=False).encode('utf8')


@app.route("/list_resources/<page>")
def list_resources(page,methods=['GET']):
    offset = int(page) * 100
    search = request.args.get('search',default="")
    classRDF = request.args.get('classRDF',default="")

    label_query = ""
    if USE_LABELS:
        label_query = """OPTIONAL{
                    ?resource rdfs:label ?l.
                }"""
    filterSearch = ""
    if search != None and search != '':
        filterSearch = f"""FILTER(REGEX(STR(?resource),"{search}","i") || REGEX(STR(?label),"{search}","i"))"""
    if classRDF != None and classRDF != '':
        query = f"""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?resource ?label where {{ 
                ?resource a <{classRDF}>.
                {label_query}
                BIND(COALESCE(?l,?resource) AS ?label)
                {filterSearch}
            }}
            LIMIT 100
            OFFSET {offset}
        """
    else:
        query = f"""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?resource ?label where {{ 
                ?resource ?p _:x2.
                {label_query}
                BIND(COALESCE(?l,?resource) AS ?label)
                {filterSearch}
            }}
            LIMIT 100
            OFFSET {offset}
        """
    sparql_resources.setQuery(query)
    # print(query)
    sparql_resources.setReturnFormat(JSON)
    results = sparql_resources.query().convert()
    resources = []
    for result in results["results"]["bindings"]:
        resource = {'uri':urllib.parse.quote(result['resource']['value']),'label':result['label']['value'],'graphdb_url':GRAPHDB_BROWSER+"?uri="+urllib.parse.quote(result['resource']['value'])+GRAPHDB_BROWSER_CONFIG+"&embedded"}
        if "http://" in resource['label'] or "https://" in resource['label']:
            resource['label'] = resource['label'].split("/")[-1].split("#")[-1]
        resources.append(resource)
    return json.dumps(resources, ensure_ascii=False).encode('utf8')


@app.route("/list_saved")
def list_saved():
    return render_template("list_saved.html",saved_queries=saved_queries)



@app.route("/list_itens_saved/<id>/<page>")
def list_itens_saved(id,page):
    return render_template("list_itens_saved.html",id=id,page=page)


@app.route("/query_saved/<id>/<page>")
def query_saved(id,page):
    offset = int(page) * 100
    id = int(id)
    item = saved_queries[id]
    query = item['query'] + f"\nOFFSET {offset}"
    sparql_resources.setQuery(query)
    # print(query)
    sparql_resources.setReturnFormat(JSON)
    results = sparql_resources.query().convert()
    resources = []
    for result in results["results"]["bindings"]:
        query_construct = item['construct_query'].replace("$URI",result[item['uri_var']]['value']) 
        resource = {'graphdb_url':GRAPHDB_BROWSER+"?query="+urllib.parse.quote(query_construct)+GRAPHDB_BROWSER_CONFIG+"&embedded"}
        for var in result:
            resource[var] = result[var]['value']
        resources.append(resource)
    return json.dumps({'vars':results['head']['vars'],'resources':resources}, ensure_ascii=False).encode('utf8')


@app.route("/browser")
def browser(methods=['GET']):
    uri = request.args.get('uri',default="")
    return render_template("browser.html",uri=uri,USE_LABELS=USE_LABELS)

@app.route("/get_properties")
def get_properties(methods=['GET']):
    uri = request.args.get('uri',default="")
    if not USE_N_ARY_RELATIONS:
        query = f"""
            SELECT ?p ?o WHERE{{
                <{uri}> ?p ?o.    
            }} ORDER BY ?p		     
        """
    else:
        query = f"""
            PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>
            select ?p ?o where {{ 
                <{uri}> ?p ?o .
                FILTER NOT EXISTS{{
                    ?o a sfz:N_ary_Relation_Class 
                }}
            }} ORDER BY ?p	     
        """
    sparql_resources.setQuery(query)
    # print(query)
    sparql_resources.setReturnFormat(JSON)
    results = sparql_resources.query().convert()
    properties = {}
    metadatas = {}
    
    for result in results["results"]["bindings"]:
        if not result['p']['value'] in properties:
            properties[result['p']['value']] = []
        properties[result['p']['value']].append([result['o']['value'],[]])

    if USE_N_ARY_RELATIONS:
        query = f"""
            PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select ?p1 ?o1 ?p2  ?o2 where {{ 
                <{uri}> ?p1 ?o_aux .
                ?o_aux a sfz:N_ary_Relation_Class;
                    rdf:objeto_referenciado ?o1;
                    ?p2 ?o2.
                FILTER(!CONTAINS(STR(?p2),"http://www.w3.org/2000/01/rdf-schema#"))
                FILTER(!CONTAINS(STR(?p2),"http://www.w3.org/2001/XMLSchema#"))
                FILTER(!CONTAINS(STR(?p2),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
                FILTER(!CONTAINS(STR(?p2),"http://www.w3.org/2002/07/owl#"))
            }}  
        """
        sparql_resources.setQuery(query)
        # print(query)
        sparql_resources.setReturnFormat(JSON)
        results = sparql_resources.query().convert()
        
        for result in results["results"]["bindings"]:
            if not result['p1']['value'] in properties:
                properties[result['p1']['value']] = []
                metadatas[result['p1']['value']] = {}
            if not result['o1']['value'] in metadatas[result['p1']['value']]:
                metadatas[result['p1']['value']][result['o1']['value']] = []
            metadatas[result['p1']['value']][result['o1']['value']].append([result['p2']['value'],result['o2']['value']])    
        
        for property in metadatas:
            for value in metadatas[property]:
                properties[property].append([value,metadatas[property][value]])
        
    propriedades_list = json.loads(propriedades())['propriedades']
    classes_list = {}
    for classe in json.loads(classes())['classes']:
        classes_list[classe['uri_raw']] = classe['label']
    return jsonify({'properties':properties,'propriedades_list':propriedades_list,'classes_list':classes_list,'graphdb_link':GRAPHDB_BROWSER+"?uri="+urllib.parse.quote(uri)+str(GRAPHDB_BROWSER_CONFIG)+"&embedded"})

@app.route("/get_income_properties")
def get_income_properties(methods=['GET']):
    uri = request.args.get('uri',default="")
    query = f"""
        SELECT ?s ?p  WHERE{{
            ?s ?p <{uri}>.    
        }} ORDER BY ?p		     
    """  
    sparql_resources.setQuery(query)
    # print(query)
    sparql_resources.setReturnFormat(JSON)
    results = sparql_resources.query().convert()  
    properties = {}
    for result in results["results"]["bindings"]:
        if not result['p']['value'] in properties:
            properties[result['p']['value']] = []
        properties[result['p']['value']].append([result['s']['value'],[]])
    return jsonify(properties)

@app.route("/get_label")
def getLabel(methods=['GET']):
    uri = request.args.get('uri',default="")
    query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?s (GROUP_CONCAT(?label;separator=".\\n") as ?label) where {{ 
                BIND(<{uri}> as ?s)
                ?s rdfs:label ?l.
            
                BIND(COALESCE(?l,?s) AS ?label)
            }} GROUP BY ?s
        """
    sparql_resources.setQuery(query)
    # print(query)
    sparql_resources.setReturnFormat(JSON)
    results = sparql_resources.query().convert()
    if len(results["results"]["bindings"]) > 0:
        label = results["results"]["bindings"][0]['label']['value']
    else:
        label = ""
    return {'label':label}

@app.route("/timeline")
def timeline(methods=['GET']):
    uri = request.args.get('uri',default="")
    return render_template("timeline.html",uri=uri)

@app.route("/get_historico")
def get_historico():
    #UPDATE PROPERTY
    uri = request.args.get('uri',default=None)
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix tl: <http://purl.org/NET/c4dm/timeline.owl#>
    prefix sfz: <http://www.sefaz.ma.gov.br/ontology/>
    SELECT ?data ?campo  ?va ?vn WHERE {
    <$uri> sfz:tem_timeLine ?tl.
    ?inst tl:timeLine ?tl;
        sfz:tem_atualizacao ?att;
        tl:atDate ?data.
    ?att a sfz:Atualiza_Propriedade;
        sfz:valor_antigo ?va;
        sfz:valor_novo ?vn;
        sfz:atributo ?campo.
    }
    ORDER BY ?data ?campo 
    """.replace("$uri",uri)
    sparql_history.setQuery(query)
    # print(query)
    sparql_history.setReturnFormat(JSON)
    results = sparql_history.query().convert()
    resources_historico_data = {}
    for result in results["results"]["bindings"]:
        data = result['data']['value']
        if not data in resources_historico_data:
            resources_historico_data[data]= {}
        if not result['campo']['value'] in resources_historico_data[data]:
            resources_historico_data[data][result['campo']['value']] = []
        resources_historico_data[data][result['campo']['value']].append({'valor_antigo': result['va']['value'],'valor_novo': result['vn']['value']})
    resources_historico_propriedade = {}
    for result in results["results"]["bindings"]:
        data = result['data']['value']
        propriedade = result['campo']['value']
        if not propriedade in resources_historico_propriedade:
            resources_historico_propriedade[propriedade]= {}
        if not data in resources_historico_propriedade[propriedade]:
            resources_historico_propriedade[propriedade][data] = []
        resources_historico_propriedade[propriedade][data].append({'valor_antigo': result['va']['value'],'valor_novo': result['vn']['value']})

    # INSERT RESOURCE
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix tl: <http://purl.org/NET/c4dm/timeline.owl#>
    prefix sfz: <http://www.sefaz.ma.gov.br/ontology/>
    SELECT DISTINCT ?data WHERE {
        <$uri> sfz:tem_timeLine ?tl.
        ?inst tl:timeLine ?tl;
            sfz:tem_atualizacao ?att;
            tl:atDate ?data.
        ?att a sfz:Insere_Tipo.
    }
    """.replace("$uri",uri)
    sparql_history.setQuery(query)
    # print(query)
    sparql_history.setReturnFormat(JSON)
    results = sparql_history.query().convert()
    for ins in results["results"]["bindings"]:
        data = ins['data']['value']
        if not data in resources_historico_data:
            resources_historico_data[data] = {}
        if not 'INS' in resources_historico_data[data]:
            resources_historico_data[data]['INS'] = []

    # INSERT PROPERTY
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix tl: <http://purl.org/NET/c4dm/timeline.owl#>
    prefix sfz: <http://www.sefaz.ma.gov.br/ontology/>
    SELECT DISTINCT ?data ?prop ?obj WHERE {
        <$uri> sfz:tem_timeLine ?tl.
        ?inst tl:timeLine ?tl;
            sfz:tem_atualizacao ?att;
            tl:atDate ?data.
        ?att a sfz:Insere_Relacionamento;
            sfz:uri_objeto_relacionado ?obj;
            sfz:atributo ?prop
    }
    """.replace("$uri",uri)
    sparql_history.setQuery(query)
    # print(query)
    sparql_history.setReturnFormat(JSON)
    results = sparql_history.query().convert()
    for ins in results["results"]["bindings"]:
        data = ins['data']['value']
        if not data in resources_historico_data:
            resources_historico_data[data] = {}
        if not 'INS_PROP' in resources_historico_data[data]:
            resources_historico_data[data]['INS_PROP'] = []
        resources_historico_data[data]['INS_PROP'].append([ins['prop']['value'],ins['obj']['value']])


    # REMOVE RESOURCE
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix tl: <http://purl.org/NET/c4dm/timeline.owl#>
    prefix sfz: <http://www.sefaz.ma.gov.br/ontology/>
    SELECT DISTINCT ?data WHERE {
        <$uri> sfz:tem_timeLine ?tl.
        ?inst tl:timeLine ?tl;
            sfz:tem_atualizacao ?att;
            tl:atDate ?data.
        ?att a sfz:Remove_Tipo.
    }
    """.replace("$uri",uri)
    sparql_history.setQuery(query)
    # print(query)
    sparql_history.setReturnFormat(JSON)
    results = sparql_history.query().convert()
    for dell in results["results"]["bindings"]:
        data = dell['data']['value']
        if not data in resources_historico_data:
            resources_historico_data[data] = {}
        if not 'DEL' in resources_historico_data[data]:
            resources_historico_data[data]['DEL'] = []

    # REMOVE PROPERTY
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix tl: <http://purl.org/NET/c4dm/timeline.owl#>
    prefix sfz: <http://www.sefaz.ma.gov.br/ontology/>
    SELECT DISTINCT ?data ?prop ?obj WHERE {
        <$uri> sfz:tem_timeLine ?tl.
        ?inst tl:timeLine ?tl;
            sfz:tem_atualizacao ?att;
            tl:atDate ?data.
        ?att a sfz:Remove_Relacionamento;
            sfz:uri_objeto_relacionado ?obj;
            sfz:atributo ?prop
    }
    """.replace("$uri",uri)
    sparql_history.setQuery(query)
    # print(query)
    sparql_history.setReturnFormat(JSON)
    results = sparql_history.query().convert()
    for ins in results["results"]["bindings"]:
        data = ins['data']['value']
        if not data in resources_historico_data:
            resources_historico_data[data] = {}
        if not 'REM_PROP' in resources_historico_data[data]:
            resources_historico_data[data]['REM_PROP'] = []
        resources_historico_data[data]['REM_PROP'].append([ins['prop']['value'],ins['obj']['value']])
    
    resources_historico_data = dict(sorted(resources_historico_data.items()))
    resources = {'resources_historico_propriedade':resources_historico_propriedade,'resources_historico_data':resources_historico_data}
    return json.dumps(resources, ensure_ascii=False).encode('utf8')


if __name__ == "__main__":
    # app.run(host='10.33.96.18',port=1111) #Colocar IP da máquina hospedeira (Servidor) aqui
    app.run(host='0.0.0.0',port=2222)
