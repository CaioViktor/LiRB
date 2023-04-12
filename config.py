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

#LOCAL
ENDPOINT_ONTOLOGY = "http://localhost:7200/repositories/ONTOLOGIA_DOMINIO"
ENDPOINT_RESOURCES = "http://localhost:7200/repositories/Test"
ENDPOINT_HISTORY = "http://localhost:7200/repositories/Test"
GRAPHDB_BROWSER = "http://localhost:7200/graphs-visualizations"
GRAPHDB_BROWSER_CONFIG = "&config=ce05fb50c18a4de69d59be186eb6acc5"
USE_N_ARY_RELATIONS = False
USE_LABELS = True 

