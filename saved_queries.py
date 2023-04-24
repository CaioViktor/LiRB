ex = {
    'description': "",#Description showed as title for the query
    'query': "", #SPARQL Query to select the data showed in the table
    'uri_var':"", # Variable's name (without "?") for select query that will be used to filter the construct query
    'construct_query': "" #Consctruct query used to cronstruct a graphical visualization. Uses the value of 'uri_var' as value for the <$URI> parameter user to filter the construct query.
}

q = {
    'description': """Who knows who?""",
    'query': """
PREFIX lirb: <https://raw.githubusercontent.com/CaioViktor/LiRB/main/lirb_ontology.ttl/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://www.example.lirb.com/> 
SELECT ?node ?k WHERE{
    {
        ?node ex:knows ?k .    
    }
    UNION{
        ?k ex:knows ?node.        
    }  
}ORDER BY ?node""",
    'uri_var':"node",
    'construct_query': """
    PREFIX lirb: <https://raw.githubusercontent.com/CaioViktor/LiRB/main/lirb_ontology.ttl/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ex: <http://www.example.lirb.com/> 

    CONSTRUCT{
        ?node ex:knows ?o.
        ?s ex:knows ?node.
    } where { 
        OPTIONAL{
            ?node ex:knows ?o .    
            FILTER(?node = <$URI>)
        }
        OPTIONAL{
            ?s ex:knows ?node.        
            FILTER(?node = <$URI>)
        }  
    }
    """
}



saved_queries = [q]
