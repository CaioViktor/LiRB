q2 = {
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

q3 = {
    'description': """Quais empresas na RFB ou SEFAZ não tem mais sócio pessoa física?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

PREFIX owl: <http://www.w3.org/2002/07/owl#>

PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?empresa ?cnpj_empresa WHERE {
{
    ?empresa a sefazma:Empresa_RFB;
        sefazma:cnpj ?cnpj_empresa;
        sefazma:tem_sociedade_juridica ?x.
        
    MINUS {
        ?empresa sefazma:tem_sociedade_fisica ?x2.
    }
 
}
UNION
{
    ?empresa a sefazma:Empresa_Cadastro;
        sefazma:cnpj ?cnpj_empresa.
        
    MINUS {
        ?empresa sefazma:tem_sociedade ?x.
        ?x a sefazma:Sociedade_PF.
 } 
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
    ?empresa ?p ?o
}WHERE {
    ?empresa ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
}
    """
}


q4 = {
    'description': """Quais empresas não estão ativas na RFB, mas estão na SEFAZ?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?estabelecimento_rfb ?cnpj_estabelecimento_rfb ?nome_fantasia_rfb ?cnpj_estabelecimento_cadastro ?nome_fantasia_cadastro ?tipo_situacao_rfb ?tipo_situacao_cadastro WHERE {

  ?estabelecimento_rfb a sefazma:Estabelecimento_RFB;
     sefazma:cnpj ?cnpj_estabelecimento_rfb;
     sefazma:nome_fantasia ?nome_fantasia_rfb;
     sefazma:tem_situacao_cadastral ?situacao_cadastral_rfb.
  
  ?situacao_cadastral_rfb rdfs:label ?tipo_situacao.
    FILTER(!CONTAINS(?tipo_situacao, 'ATIVA'))
    BIND(REPLACE(STR(?tipo_situacao),"-.*","") as ?tipo_situacao_rfb) 
    
 ?estabelecimento_cadastro a sefazma:Estabelecimento_Cadastro;
        sefazma:cnpj ?cnpj_estabelecimento_cadastro;
        sefazma:nome_fantasia ?nome_fantasia_cadastro;
        sefazma:tem_situacao_cadastral ?situacao_cadastral_cadastro.
  
  ?situacao_cadastral_cadastro sefazma:tipo_situacao ?tipo_situacao_cadastro.
    
  ?estabelecimento_rfb owl:sameAs  ?estabelecimento_cadastro.
    FILTER((?tipo_situacao_rfb != ?tipo_situacao_cadastro) && ?tipo_situacao_cadastro = 'ATIVA')


}
LIMIT 100""",
    'uri_var':"estabelecimento_rfb",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?estabelecimento_rfb sefazma:tem_situacao_cadastral ?situacao_cadastral_rfb.
    ?estabelecimento_cadastro sefazma:tem_situacao_cadastral ?situacao_cadastral_cadastro.
     ?estabelecimento_rfb owl:sameAs  ?estabelecimento_cadastro.
    
} WHERE {

  ?estabelecimento_rfb a sefazma:Estabelecimento_RFB;
     sefazma:tem_situacao_cadastral ?situacao_cadastral_rfb.
  
  ?situacao_cadastral_rfb rdfs:label ?tipo_situacao.
    FILTER(!CONTAINS(?tipo_situacao, 'ATIVA'))
    BIND(REPLACE(STR(?tipo_situacao),"-.*","") as ?tipo_situacao_rfb) 
    
 ?estabelecimento_cadastro a sefazma:Estabelecimento_Cadastro;
        sefazma:tem_situacao_cadastral ?situacao_cadastral_cadastro.
  
  ?situacao_cadastral_cadastro sefazma:tipo_situacao ?tipo_situacao_cadastro.
    
  ?estabelecimento_rfb owl:sameAs  ?estabelecimento_cadastro.
    FILTER((?tipo_situacao_rfb != ?tipo_situacao_cadastro) && ?tipo_situacao_cadastro = 'ATIVA')
    FILTER(?estabelecimento_rfb = <$URI>)

}
    """
}


q5 = {
    'description': """Quais organizações são públicas?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?empresa_publica ?nome WHERE {
    {
    ?empresa_publica a sefazma:Ente_Publico;
                     rdfs:label ?nome.
    }
    UNION
    {
        ?empresa_publica a foaf:Organization;
                     rdfs:label ?nome;
                     sefazma:tem_natureza_legal ?natureza_legal.
   		?natureza_legal sefazma:codigo_natureza_legal ?codigo;
    FILTER(?codigo = "201-1"^^xsd:string || ?codigo = "2011"^^xsd:decimal)
    }
}

LIMIT 100""",
    'uri_var':"empresa_publica",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
}
    """
}

q6 = {
    'description': """Quais situações cadastrais da RFB são incompatíveis com as existentes na SEFAZ?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?estabelecimento_rfb ?estabelecimento_cadastro ?cnpj_rfb ?cnpj_cadastro ?nome_fantasia_rfb ?nome_fantasia_cadastro ?situacao_rfb ?situacao_cadastro   WHERE {

 ?estabelecimento_rfb a sefazma:Estabelecimento_RFB;
     sefazma:cnpj ?cnpj_rfb;
     sefazma:nome_fantasia ?nome_fantasia_rfb;
     sefazma:tem_situacao_cadastral ?situacao_rfb.
    
     ?situacao_rfb rdfs:label ?tipo_situacao.
    BIND(REPLACE(STR(?tipo_situacao),"-.*","") as ?tipo_situacao_rfb) 
    
    ?estabelecimento_cadastro owl:sameAs ?estabelecimento_rfb.
    ?estabelecimento_cadastro a sefazma:Estabelecimento_Cadastro;
            sefazma:cnpj ?cnpj_cadastro;
            sefazma:nome_fantasia ?nome_fantasia_cadastro;
            sefazma:tem_situacao_cadastral ?situacao_cadastro.
    
    ?situacao_cadastro rdfs:label ?tipo_situacao2.
    BIND(REPLACE(STR(?tipo_situacao2),"-.*","") as ?tipo_situacao_cadastro) 
   
    FILTER(?tipo_situacao_rfb != ?tipo_situacao_cadastro)
}
LIMIT 100""",
    'uri_var':"estabelecimento_rfb",
    'construct_query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?estabelecimento_rfb sefazma:tem_situacao_cadastral ?situacao_rfb.
    ?estabelecimento_rfb owl:sameAs ?estabelecimento_cadastro.
    ?estabelecimento_cadastro sefazma:tem_situacao_cadastral ?situacao_cadastro.
}WHERE {

 ?estabelecimento_rfb a sefazma:Estabelecimento_RFB;
     sefazma:tem_situacao_cadastral ?situacao_rfb.
	
   ?estabelecimento_rfb owl:sameAs ?estabelecimento_cadastro.
    ?estabelecimento_cadastro a sefazma:Estabelecimento_Cadastro;
            sefazma:tem_situacao_cadastral ?situacao_cadastro.
    FILTER(?estabelecimento_rfb = <$URI>)
}
LIMIT 10
    """
}

q7 = {
    'description': """Quem são os contribuintes?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?contribuinte ?inscricao_estadual WHERE {
    ?contribuinte a sefazma:Contribuinte_Geral;
          rdfs:label ?inscricao_estadual.
}
LIMIT 100""",
    'uri_var':"contribuinte",
    'construct_query': """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
}
    """
}

q8 = {
    'description': """Quem são os contribuintes Simples Nacional?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?contribuinte ?inscricao_estadual WHERE {
    ?contribuinte a sefazma:Simples_Nacional;
          rdfs:label ?inscricao_estadual.
}

LIMIT 100""",
    'uri_var':"contribuinte",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
}
    """
}

q9 = {
    'description': """Quem são os contribuintes Subistituto Tributário?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?contribuinte ?inscricao_estadual WHERE {
    ?contribuinte a sefazma:Substituto_Tributario;
          rdfs:label ?inscricao_estadual.
}
LIMIT 100""",
    'uri_var':"contribuinte",
    'construct_query': """
   PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
} 
    """
}

q10 = {
    'description': """Quem são os Não Contribuintes?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?contribuinte ?label WHERE {
    ?contribuinte a sefazma:Nao_Contribuinte;
          rdfs:label ?label.
}
LIMIT 100""",
    'uri_var':"contribuinte",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?o1 = <$URI>)
} 
    """
}


q11 = {
    'description': """Quais Empresas na SEFAZ não tem Sócios?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?empresa ?label WHERE {
    ?empresa a sefazma:Empresa_Cadastro;
    	rdfs:label ?label.
    MINUS {
        ?empresa sefazma:tem_sociedade ?sociedade.
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
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
} 
    """
}

q12 = {
    'description': """Quais são os órgãos públicos por esfera do poder (Executivo, Legislativo e Judiciário) e por nível (Federal, Estadual e Municipal)?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?ente_publico ?ente ?esfera ?nivel WHERE {
    ?ente_publico a sefazma:Ente_Publico;
                  rdfs:label ?ente;
    			  sefazma:esfera ?esfera;
                  sefazma:nivel ?nivel.
}ORDER BY ?esfera ?nivel
LIMIT 100""",
    'uri_var':"ente_publico",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
} 
    """
}


q13 = {
    'description': """Quem Vende para os órgãos públicos?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?fornecedor ?fornecedor_compra ?cnpj_cpf WHERE {
    ?compra a sefazma:Compra_Publica;
            sefazma:tem_fornecedor ?fornecedor.
    ?fornecedor rdfs:label ?fornecedor_compra;
                sefazma:cnpj_cpf ?cnpj_cpf.
}
LIMIT 100""",
    'uri_var':"fornecedor",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?compra sefazma:tem_fornecedor ?fornecedor.
}WHERE {
    ?compra a sefazma:Compra_Publica;
            sefazma:tem_fornecedor ?fornecedor.
    ?fornecedor rdfs:label ?fornecedor_compra;
                sefazma:cnpj_cpf ?cnpj_cpf.
    FILTER(?fornecedor = <$URI>)
}
    """
}


q14 = {
    'description': """Quais fornecedores estão com alguma restrição ou sanção nas fontes de dados integradas: (CEI, CEIS ou TCU)?""",
    'query': """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?fornecedor ?fornecedor_restrito ?cnpj_cpf ?fonte WHERE {
     ?fornecedor a sefazma:Fornecedor_Restrito;
                 foaf:name ?fornecedor_restrito;
                 sefazma:cnpj_cpf ?cnpj_cpf.
 
    BIND(IF(CONTAINS(STR(?fornecedor),"TCU"),"TCU",IF(CONTAINS(STR(?fornecedor),"CEI"),"CEI",IF(CONTAINS(STR(?fornecedor),"CEIS"),"CEIS",""))) as ?fonte)
}
LIMIT 100""",
    'uri_var':"fornecedor",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
} 
    """
}


q15 = {
    'description': """Quais os Fornecedores Maranheses?""",
    'query': """
     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?fornecedor_restrito ?nome WHERE { 
	?fornecedor_restrito a sefazma:Fornecedor_Restrito ;
             	rdfs:label ?nome;
    			sefazma:tem_unidade_federativa ?uf.
    
    ?uf a sefazma:Unidade_Federativa;
        rdfs:label ?estado.
    
    FILTER(?estado = "MA")
    
}
LIMIT 100""",
    'uri_var':"fornecedor_restrito",
    'construct_query': """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT{
    ?o1 ?p ?o
}WHERE {
    ?o1 ?p ?o.
    FILTER(isUri(?o))
    FILTER(?p != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    FILTER(?o1 = <$URI>)
} 
    """
}


saved_queries = [q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15]
