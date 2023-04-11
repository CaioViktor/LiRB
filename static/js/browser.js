const propriedadesDestaque = ['http://www.w3.org/2000/01/rdf-schema#label','http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.w3.org/2000/01/rdf-schema#comment','http://dbpedia.org/ontology/thumbnail','http://xmlns.com/foaf/0.1/thumbnail','http://xmlns.com/foaf/0.1/img','http://www.sefaz.ma.gov.br/ontology/tem_timeLine'];
let propriedades_list = null;
let classes_list = null;
let income = null;
const data = d3.json("/get_properties?uri="+encodeURI(uri)).then(function(dataR){
	let data = dataR;
	
    classes_list = dataR['classes_list'];
    propriedades_list = dataR['propriedades_list'];
    let properties = dataR['properties'];
    
    $("#grafoVisual")[0].href=dataR['graphdb_link'];

    if('http://www.sefaz.ma.gov.br/ontology/tem_timeLine' in properties){//Recurso tem timeline
        $("#timeline")[0].href='timeline?uri='+encodeURI(uri);
        $("#timeline").show();
    }


    if(['http://dbpedia.org/ontology/thumbnail','http://xmlns.com/foaf/0.1/thumbnail','http://xmlns.com/foaf/0.1/img'].some(el=> el in properties) ){//Thumbnails
        let row = '<div id="thumbs" class="row">';    
        ['http://dbpedia.org/ontology/thumbnail','http://xmlns.com/foaf/0.1/thumbnail','http://xmlns.com/foaf/0.1/img'].forEach(function(attr){
            if(attr in dataR['properties']){
                    dataR['properties'][attr].forEach(function(d){
                        row += '<a href="'+encodeURI(d[0])+'" target="_blank"><img src="'+d[0]+'" alt="'+d[0]+'" title="'+d[0]+'" class="thumbnail"/></a>';
                    });
                }
            });
        row += '</div>';
        $('#propriedades_destaque').append(row);
        
    }
    
    if('http://www.w3.org/2000/01/rdf-schema#label' in properties){//Labels
        $(".header-table>b").text(properties['http://www.w3.org/2000/01/rdf-schema#label'][0][0]);
        $("#nav-label").append(properties['http://www.w3.org/2000/01/rdf-schema#label'][0][0]);
        let row = '<div id="label" class="row"><i class="fa-solid fa-tag" title="Nomes"></i>';
        dataR['properties']['http://www.w3.org/2000/01/rdf-schema#label'].forEach(function(d){
            row += '<p title="Título"><b>'+d[0]+'</b></p>';
        });
        row += '</div>';
        $('#propriedades_destaque').append(row);
    }
    
    
    if('http://www.w3.org/2000/01/rdf-schema#comment' in properties){//Comments
        let row = '<div id="comment">"';
        dataR['properties']['http://www.w3.org/2000/01/rdf-schema#comment'].forEach(function(d){
            row += '<p>'+d[0]+'</p>';
        });
        row += '"</div>';
        $('#propriedades_destaque').append(row);
    }

    $('#propriedades_destaque').append('<div id="uri"><p title="URI" ><i class="fa-solid fa-link"></i>'+uri+'</p></div>');//URIss

    if('http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in properties){//Tipos
        let row = '<div id="type">';
        row += '<b title="http://www.w3.org/1999/02/22-rdf-syntax-ns#type">Tipos</b>';
        row += '<div id="types" class="row">'
        dataR['properties']['http://www.w3.org/1999/02/22-rdf-syntax-ns#type'].forEach(function(d){
            let label = classes_list[d[0]];
            if(!(d[0] in classes_list)){
                label = d[0].split("/");
                label = label[label.length-1];
                label = label.split("#")
                label = label[label.length-1].replaceAll("_"," ");
            }
            row += '<a title="'+d[0]+'" href="/resources/0/?classRDF='+encodeURI(d[0])+'&label='+classes_list[d[0]]+'" id="'+d[0]+'" class="types">'+label+'</a>';
        });
        row += '</div>';
        row += '</div>';
        $('#propriedades_destaque').append(row);
    }
    let idx_prop = 0;
    for(property in dataR['properties']){//Demais propriedades
        if(!(propriedadesDestaque.includes(property))){
            let row = '<div id="'+property+'">';
            if(property in propriedades_list)//Propriedade tem label definida
                row += '<b title="'+property+'">'+propriedades_list[property]+' ('+dataR['properties'][property].length+') <i class="fa-solid fa-arrow-right"></i></b>';
            else{//Propriedade tem não label definida
                let label = property.split("/");
                label = label[label.length-1];
                label = label.split("#")
                label = label[label.length-1].replaceAll("_"," ");
                row += '<b title="'+property+'">'+label+' ('+dataR['properties'][property].length+') <i class="fa-solid fa-arrow-right"></i></b>';
            }
            row += '<ul>'
            let count_value = 0;
            dataR['properties'][property].forEach(function(d){
                if(count_value == 10)
                    row+="<details><summary>Mais ("+(dataR['properties'][property].length - count_value)+")</summary>";
                
                if(d[0].includes('http')){ //Propriedade é uma objectProperty
                    if(['.png','.jpeg','.jpg','.gif','.svg','.ico','.apng','.bmp'].some(typ=>d[0].includes(typ))){//Propriedade é um link para uma imagem
                        row += '<li><a href="'+encodeURI(d[0])+'" target="_blank"><img src="'+d[0]+'" alt="'+d[0]+'" title="'+d[0]+'" class="thumbnail"/></a></li>';
                    }
                    else{//Propriedade é uma objectProperty qualquer
                        row += '<li><a id="link_'+idx_prop+'_'+count_value+'" href="/browser?uri='+encodeURI(d[0])+'">'+d[0]+'</a></li>';
                        const current_idx = idx_prop+'_'+count_value;
                        if(USE_LABELS){
                            label_object = d3.json("/get_label?uri="+encodeURI(d[0])).then(function(l_obj){
                                if(l_obj['label'].trim().length > 0)
                                    $('#link_'+current_idx).text(l_obj['label']);
                            });
                        }
                    }
                }
                else//Propriedade é uma datatypeProperty
                    row += '<li><p>'+d[0]+'</p></li>';
                if(d[1].length > 0){//Propriedade tem metadados
                    row += '<ul>'
                    d[1].forEach(function(meta){
                        let label = propriedades_list[meta[0]];
                        if(!(meta[0] in propriedades_list)){
                            label = meta[0].split("/");
                            label = label[label.length-1];
                            label = label.split("#")
                            label = label[label.length-1].replaceAll("_"," ");
                        }
                        row += '<li title="'+meta[0]+'"><b>'+label+':</b><p> '+meta[1]+'</p></li>';
                    });
                    row += '</ul>'
                }
                if(count_value == dataR['properties'][property].length)
                    row+="</details>";
                count_value+=1;
            });
            row += '</ul>'
            row += '</div>';
            idx_prop+=1;
            $('#propriedades_geral').append(row);
        }
    }
	$("#loading").hide();
    income = d3.json("/get_income_properties?uri="+encodeURI(uri)).then(function(dataR){
        let idx_prop = 0;
        for(property in dataR){//Demais propriedades
            let row = '<div id="'+property+'">';
            if(property in propriedades_list)//Propriedade tem label definida
                row += '<b title="'+property+'"><i class="fa-solid fa-arrow-left"></i> '+propriedades_list[property]+'</b> ('+dataR[property].length+")";
            else{//Propriedade tem não label definida
                let label = property.split("/");
                label = label[label.length-1];
                label = label.split("#")
                label = label[label.length-1].replaceAll("_"," ");
                row += '<b title="'+property+'"><i class="fa-solid fa-arrow-left"></i> '+label+'</b> ('+dataR[property].length+")";
            }
            row += '<ul>'
            let count_value = 1;
            dataR[property].forEach(function(d){
                if(count_value == 10)
                    row+="<details><summary>Mais ("+(dataR[property].length - count_value)+")</summary>";
                
                if(d[0].includes('http')){ //Propriedade é uma objectProperty
                    if(['.png','.jpeg','.jpg','.gif','.svg','.ico','.apng','.bmp'].some(typ=>d[0].includes(typ))){//Propriedade é um link para uma imagem
                        row += '<li><a href="'+encodeURI(d[0])+'" target="_blank"><img src="'+d[0]+'" alt="'+d[0]+'" title="'+d[0]+'" class="thumbnail"/></a></li>';
                    }
                    else{//Propriedade é uma objectProperty qualquer
                        row += '<li><a id="link_income_'+idx_prop+'_'+count_value+'" href="/browser?uri='+encodeURI(d[0])+'">'+d[0]+'</a></li>';
                        const current_idx = idx_prop+'_'+count_value;
                        if(USE_LABELS){
                            label_object = d3.json("/get_label?uri="+encodeURI(d[0])).then(function(l_obj){
                                if(l_obj['label'].trim().length > 0)
                                    $('#link_income_'+current_idx).text(l_obj['label']);
                            });
                        }
                    }
                }
                if(count_value == dataR[property].length)
                    row+="</details>";
                count_value+=1;
            });
            row += '</ul>'
            row += '</div>';
            idx_prop+=1;
            $('#propriedades_income').append(row);
    
        }
        return dataR;
    });
	return data;
});




