const propriedadesDestaque = ['http://www.w3.org/2000/01/rdf-schema#label','http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.w3.org/2000/01/rdf-schema#comment','http://dbpedia.org/ontology/thumbnail','http://xmlns.com/foaf/0.1/thumbnail','http://xmlns.com/foaf/0.1/img','http://www.arida.ufc.br/ontology/timeline/has_timeLine'];
let properties_list = null;
let classes_list = null;
let income = null;
const data = d3.json("/get_properties?uri="+encodeURI(uri)+"&expand_sameas="+expand_sameas).then(function(dataR){
	let data = dataR;
	
    classes_list = dataR['classes_list'];
    properties_list = dataR['properties_list'];
    let properties = dataR['properties'];
    
    $("#visualGraph")[0].href=dataR['graphdb_link'];

    if('http://www.arida.ufc.br/ontology/timeline/has_timeLine' in properties){//Resource has timeline
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
        $('#highlight_properties').append(row);
        
    }
    
    if('http://www.w3.org/2000/01/rdf-schema#label' in properties){//Labels
        $(".header-table>b").text(properties['http://www.w3.org/2000/01/rdf-schema#label'][0][0]);
        $("#nav-label").append(properties['http://www.w3.org/2000/01/rdf-schema#label'][0][0]);
        let row = '<div id="label" class="row"><i class="fa-solid fa-tag" title="Nomes"></i>';
        dataR['properties']['http://www.w3.org/2000/01/rdf-schema#label'].forEach(function(d){
            row += '<p title="Label"><b>'+d[0]+'</b></p>';
        });
        row += '</div>';
        $('#highlight_properties').append(row);
    }
    
    if('http://www.w3.org/2000/01/rdf-schema#comment' in properties){//Comments
        let row = '<div id="comment">"';
        dataR['properties']['http://www.w3.org/2000/01/rdf-schema#comment'].forEach(function(d){
            row += '<p>'+d[0]+'</p>';
        });
        row += '"</div>';
        $('#highlight_properties').append(row);
    }

    $('#highlight_properties').append('<div id="uri"><p title="URI" ><i class="fa-solid fa-link"></i>'+uri+'</p></div>');//URIss

    if('http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in properties){//Types
        let row = '<div id="type">';
        row += '<b title="http://www.w3.org/1999/02/22-rdf-syntax-ns#type">Types</b>';
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
        $('#highlight_properties').append(row);
    }
    let idx_prop = 0;
    for(property in dataR['properties']){//Others properties
        if(!(propriedadesDestaque.includes(property))){
            let row = '<div id="'+property+'">';
            if(property in properties_list)//Property has label
                row += '<b title="'+property+'">'+properties_list[property]+' ('+dataR['properties'][property].length+') <i class="fa-solid fa-arrow-right"></i></b>';
            else{//Property don't have label
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
                    row+="<details><summary>More ("+(dataR['properties'][property].length - count_value)+")</summary>";
                
                if(d[0].includes('http')){ //Properties is an objectProperty
                    if(['.png','.jpeg','.jpg','.gif','.svg','.ico','.apng','.bmp'].some(typ=>d[0].includes(typ))){//Property is a image link
                        row += '<li><a href="'+encodeURI(d[0])+'" target="_blank"><img src="'+d[0]+'" alt="'+d[0]+'" title="'+d[0]+'" class="thumbnail"/></a></li>';
                    }
                    else{//Properties is another objectProperty
                        row += '<li><a id="link_'+idx_prop+'_'+count_value+'" href="/browser?uri='+encodeURI(d[0])+"&expand_sameas="+expand_sameas+'">'+d[0]+'</a></li>';
                        const current_idx = idx_prop+'_'+count_value;
                        if(USE_LABELS){
                            label_object = d3.json("/get_label?uri="+encodeURI(d[0])).then(function(l_obj){
                                if(l_obj['label'].trim().length > 0)
                                    $('#link_'+current_idx).text(l_obj['label']);
                            });
                        }
                    }
                }
                else//Properties is a datatypeProperty
                    row += '<li><p id="link_'+idx_prop+'_'+count_value+'">'+d[0]+'</p></li>';
                    const current_idx = idx_prop+'_'+count_value;
                        if(USE_LABELS && d[0].includes('http')){
                            label_object = d3.json("/get_label?uri="+encodeURI(d[0])).then(function(l_obj){
                                if(l_obj['label'].trim().length > 0)
                                    $('#link_'+current_idx).text(l_obj['label']);
                            });
                        }
                if(d[1].length > 0){//Property has metadata (lirb:N_ary_Relation_Class)
                    row += '<ul>';
                    d[1].forEach(function(meta){
                        if(meta[0] != 'https://raw.githubusercontent.com/CaioViktor/LiRB/main/lirb_ontology.ttl/value'){
                            let label = properties_list[meta[0]];
                            if(!(meta[0] in properties_list)){
                                label = meta[0].split("/");
                                label = label[label.length-1];
                                label = label.split("#")
                                label = label[label.length-1].replaceAll("_"," ");
                            }
                            row += '<li title="'+meta[0]+'"><b>'+label+':</b><p> '+meta[1]+'</p></li>';
                        }
                    });
                    row += '</ul>';
                }
                if(count_value == dataR['properties'][property].length)
                    row+="</details>";
                count_value+=1;
            });
            row += '</ul>';
            row += '</div>';
            idx_prop+=1;
            $('#general_properties').append(row);
        }
    }
	$("#loading").hide();
    income = d3.json("/get_income_properties?uri="+encodeURI(uri)+"&expand_sameas="+expand_sameas).then(function(dataR){
        let idx_prop = 0;
        for(property in dataR){//Others properties
            let row = '<div id="'+property+'">';
            if(property in properties_list)//Property has label
                row += '<b title="'+property+'"><i class="fa-solid fa-arrow-left"></i> '+properties_list[property]+'</b> ('+dataR[property].length+")";
            else{//Property dont have label
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
                    row+="<details><summary>More ("+(dataR[property].length - count_value)+")</summary>";
                
                if(d[0].includes('http')){ //Properties is an objectProperty
                    if(['.png','.jpeg','.jpg','.gif','.svg','.ico','.apng','.bmp'].some(typ=>d[0].includes(typ))){//Property is a image link
                        row += '<li><a href="'+encodeURI(d[0])+'" target="_blank"><img src="'+d[0]+'" alt="'+d[0]+'" title="'+d[0]+'" class="thumbnail"/></a></li>';
                    }
                    else{//Properties is another objectProperty
                        row += '<li><a id="link_income_'+idx_prop+'_'+count_value+'" href="/browser?uri='+encodeURI(d[0])+"&expand_sameas="+expand_sameas+'">'+d[0]+'</a></li>';
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
            $('#income_properties').append(row);
        }
        return dataR;
    });
	return data;
});




