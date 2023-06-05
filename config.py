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
# HIGHLIGHT_CLASSES = [] #A list with URIs of highlighted classes
# EXPAND_SAMEAS = False #Set True if needed to show all the properties for a resource, including its owl:sameAs's properties
# EXPAND_SAMEAS_TIMELINES = False #Set True if needed to show all events in history for a resource, including its owl:sameAs's properties
#

#LOCAL
ENDPOINT_ONTOLOGY = "http://localhost:7200/repositories/artigo"
ENDPOINT_RESOURCES = "http://localhost:7200/repositories/artigo"
ENDPOINT_HISTORY = "http://localhost:7200/repositories/artigo"
GRAPHDB_BROWSER = "http://localhost:7200/graphs-visualizations"
GRAPHDB_BROWSER_CONFIG = ""
USE_N_ARY_RELATIONS = True
USE_LABELS = True 
HIGHLIGHT_CLASSES = ['http://www.example.lirb.com/Person','http://www.example.lirb.com/Company']
EXPAND_SAMEAS = True
EXPAND_SAMEAS_TIMELINES = True

