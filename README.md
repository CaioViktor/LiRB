# LiRB
![LIght Rdf Browser](https://github.com/CaioViktor/LiRB/blob/main/static/images/logo.png)

LIght Rdf Browser (LiRB) is a lightweight interface for interactive browsing over Knowledge Graphs (KGs) RDF. LiRB features a text-based Web interface, providing a navigation experience similar to traditional Web pages, promoting a lower learning curve for users.

LiRB uses simple and fast queries, being ideal for the browsing of massive or virtual KGs. In addition, the tool also allows the abstraction of N-ary relationships to represent the semantics of  relationship’s properties. More over, LiRB have support to presents the results of saved queries to the user. Finally, LiRB also supports the feature of displaying events Timelines of resource in the KG.

## To Configurate the browser 
1. Configure the endpoints to be queried and visualization parameters in the file ["config.py"](https://github.com/CaioViktor/LiRB/blob/main/config.py) following the instructions.
2. Define the saved queries in the file ["saved_queries.py"](https://github.com/CaioViktor/LiRB/blob/main/saved_queries.py)
3. Set the host address in the file ["server.sh"](https://github.com/CaioViktor/LiRB/blob/main/server.sh)
* Obs.: The configuration files already contain example configurations for the demo KG.
## To run the browser
1. Make sure that the endpoints specified in the configurations are accessible.
2. in the application's root directory in the therminal, run the command:
   > ./server.sh
3. Access the address provided in the configuration file ["server.sh"](https://github.com/CaioViktor/LiRB/blob/main/server.sh)
   
## Demo
1. List for select classes
   ![List for select classes](https://github.com/CaioViktor/LiRB/blob/main/examples/classes_list.png)
2. Browsing resource on LiRB (abstracting N-ary relation):
   ![resource on lirb](https://github.com/CaioViktor/LiRB/blob/main/examples/resource_lirb.png)
* Visual graph on GraphDB:
    ![Visual graph](https://github.com/CaioViktor/LiRB/blob/main/examples/resource_graph.png)
3. Browsing resource on LiRB (not abstracting N-ary relation):
   ![resource on lirb](https://github.com/CaioViktor/LiRB/blob/main/examples/resource_no_nary.png)
* N-ary resource:
  ![n-ary resource](https://github.com/CaioViktor/LiRB/blob/main/examples/nary_resource.png)
4. Saved queries:
   1. List of saved queries:
    ![list](https://github.com/CaioViktor/LiRB/blob/main/examples/saved_queries.png)
   2. Query result:
    ![result](https://github.com/CaioViktor/LiRB/blob/main/examples/saved_query_result.png)
   3. Query fragment on GraphDB:
    ![graphdb](https://github.com/CaioViktor/LiRB/blob/main/examples/saved_query_graph.png)
5. Timelines from a resource:
   1. All properties:
   ![all](https://github.com/CaioViktor/LiRB/blob/main/examples/timeline.png)
   2. Filtering property:
   ![filter][https://github.com/CaioViktor/LiRB/blob/main/examples/timeline_filter.png]