ex = {
    'description': "",#Description showed as title for the query
    'query': "", #SPARQL Query to select the data showed in the table
    'filters_vars': [],# A list of tuples containing variables to be used as filters in the interface. The tuples should have the order ["?var_name","type"]. The accepted types are :"string", "numeric" and "date".
    'uri_var':"", # Variable's name (without "?") for select query that will be used to filter the construct query
    'construct_query': "" #Consctruct query used to cronstruct a graphical visualization. Uses the value of 'uri_var' as value for the <$URI> parameter user to filter the construct query.
}

q = {
    'description': """List name, age and birthday from known persons""",
    'query': """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ex: <http://www.example.lirb.com/> 
    SELECT ?node ?name ?age ?birthday WHERE{
        ?node ex:hasName ?name.
        OPTIONAL{ ?node ex:hasAge ?age1.}
        BIND(COALESCE(?age1,"-") AS ?age)
        OPTIONAL{ ?node ex:hasBirthday ?birthday1.}
        BIND(COALESCE(?birthday1,"-") AS ?birthday)
    }ORDER BY ?node
    """,
    'filters_vars':[["name","string"],["age","numeric"],["birthday","date"]],
    'uri_var':"node",
    'construct_query': """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
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
