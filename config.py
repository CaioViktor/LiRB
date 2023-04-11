# LIght Rdf Browser (LiRB) 
# Repository configuration file
#
#
#

#Default configuration
#
# ENDPOINT_ONTOLOGY = "http://localhost:7200/repositories/YOUR"#Endpoint for ontology
# ENDPOINT_RESOURCES = "http://localhost:7200/repositories/YOUR"#Endpoint for resources
# ENDPOINT_HISTORY = "http://localhost:7200/repositories/YOUR"#Endpoint for history
# GRAPHDB_BROWSER = "http://localhost:7200/graphs-visualizations"#URL for browser graph-visualization
# GRAPHDB_BROWSER_CONFIG = '' #set '' if uses default graph-visualization, '&config=ID' for custom graph-visualization config
# USE_N_ARY_RELATIONS = True #Read n-ary relations as metadata
# USE_LABELS = True #Set True to get labels for resources. When querying virtual repositories maybe be better set to False
#
#

#PROD
# ENDPOINT_ONTOLOGY = "http://10.33.96.18:7200/repositories/ONTOLOGIA_DOMINIO"
# ENDPOINT_RESOURCES = "http://10.33.96.18:7200/repositories/GRAFO_SEFAZMA_PRODUCAO"
# GRAPHDB_BROWSER = "http://10.33.96.18:7200/graphs-visualizations"
# GRAPHDB_BROWSER_CONFIG = "&config=63b76b9865064cd8a9775e1e2f46ff4d"
# ENDPOINT_HISTORY = "http://10.33.96.18:7200/repositories/GRAFO_SEFAZMA_PRODUCAO"
# USE_N_ARY_RELATIONS = False

#LOCAL
ENDPOINT_ONTOLOGY = "http://localhost:7200/repositories/ONTOLOGIA_DOMINIO"
ENDPOINT_RESOURCES = "http://localhost:7200/repositories/Endereco"
ENDPOINT_HISTORY = "http://localhost:7200/repositories/Endereco"
GRAPHDB_BROWSER = "http://localhost:7200/graphs-visualizations"
GRAPHDB_BROWSER_CONFIG = "&config=ce05fb50c18a4de69d59be186eb6acc5"
USE_N_ARY_RELATIONS = False
USE_LABELS = True 
# ENDPOINT_ONTOLOGY = "http://localhost:7200/repositories/Test"
# ENDPOINT_RESOURCES = "http://localhost:7200/repositories/Test"
# ENDPOINT_HISTORY = "http://localhost:7200/repositories/Test"
# GRAPHDB_BROWSER = "http://localhost:7200/graphs-visualizations"
# GRAPHDB_BROWSER_CONFIG = "&config=ce05fb50c18a4de69d59be186eb6acc5"
# USE_N_ARY_RELATIONS = True


#Timeline
#ENDPOINT_ONTOLOGY = "http://10.33.96.18:7200/repositories/ONTOLOGIA_DOMINIO"
#ENDPOINT_RESOURCES = "http://10.33.96.18:7200/repositories/Estudo_Timeline"
#ENDPOINT_HISTORY = "http://10.33.96.18:7200/repositories/Estudo_Timeline"
#GRAPHDB_BROWSER = "http://10.33.96.18:7200/graphs-visualizations"
#GRAPHDB_BROWSER_CONFIG = "&config=63b76b9865064cd8a9775e1e2f46ff4d"
#USE_N_ARY_RELATIONS = True


# EXTRACAD
# ENDPOINT_ONTOLOGY = "http://10.33.96.18:7200/repositories/ONTOLOGIA_EXTRACADASTRO"
# ENDPOINT_RESOURCES = "http://10.33.96.18:7200/repositories/GRAFO_EXTRACADASTRO"
# ENDPOINT_HISTORY = "http://10.33.96.18:7200/repositories/GRAFO_EXTRACADASTRO"
# GRAPHDB_BROWSER = "http://10.33.96.18:7200/graphs-visualizations"
# GRAPHDB_BROWSER_CONFIG = "&config=63b76b9865064cd8a9775e1e2f46ff4d"
# USE_N_ARY_RELATIONS = False

##VEKG
# ENDPOINT_ONTOLOGY = "http://10.33.96.18:7200/repositories/VEKG"
# ENDPOINT_RESOURCES = "http://10.33.96.18:7200/repositories/VEKG"
# ENDPOINT_HISTORY = "http://10.33.96.18:7200/repositories/VEKG"
# GRAPHDB_BROWSER = "http://10.33.96.18:7200/graphs-visualizations"
# GRAPHDB_BROWSER_CONFIG = "&config=63b76b9865064cd8a9775e1e2f46ff4d"
# USE_N_ARY_RELATIONS = False
