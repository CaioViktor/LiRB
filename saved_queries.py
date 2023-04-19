ex = {
    'description': "",#Description showed as title for the query
    'query': "", #SPARQL Query to select the data showed in the table
    'uri_var':"", # Variable's name (without "?") for select query that will be used to filter the construct query
    'construct_query': "" #Consctruct query used to cronstruct a graphical visualization. Uses the value of 'uri_var' as value for the <$URI> parameter user to filter the construct query.
}

q = {
    'description': """Quais empresas de CNAEs de incidência de ICMS existem na RFB e não existem na SEFAZ?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?empresa ?empresa_ ?atividadeICMS WHERE {
    
    ?empresa a sefazma:Estabelecimento_RFB;
             rdfs:label ?empresa_;
      	sefazma:tem_atividade_economica_principal|sefazma:tem_atividade_economica_secundaria ?atividadeICMS.

    ?atividadeICMS a sefazma:Atividade_ICMS.
    
  MINUS {
	?empresa owl:sameAs ?empresaSEFAZ.       
    ?empresaSEFAZ a sefazma:Empresa_Cadastro.
  }

}
LIMIT 100""",
    'uri_var':"empresa",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?empresa sefazma:tem_atividade_economica_isenta ?atividadeICMS.
    ?empresa ?p ?o.
}WHERE {
    ?empresa a sefazma:Estabelecimento_RFB;
      	sefazma:tem_atividade_economica_principal|sefazma:tem_atividade_economica_secundaria ?atividadeICMS.
    ?atividadeICMS a sefazma:Atividade_ICMS.
    ?empresa ?p ?o
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?empresa = <$URI>)
}
    """
}



saved_queries = [q]
