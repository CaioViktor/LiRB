const label = d3.json("/get_label?uri="+encodeURI(uri)).then(function(dataR){
    $("#label_resource")[0].innerHTML=": <b><i>" +dataR.label+"</i></b>";
    return dataR.label
});
const data = d3.json("/get_history?uri="+encodeURI(uri)).then(function(dataR){
	let data = dataR;
    
    let count = 0;
    let content = '<div id="timeline_all" class="timeline">';//Timeline for all properties
    content+='<div class="timeline__wrap">';
    content+='<div class="timeline__items">';
    for(dataI in dataR['resources_history_date']){//Loop to get all dates for all properties
        let date = new Date(dataI);
        content+='<div class="timeline__item">';
        content+='<div class="timeline__content">';
        content+= '<h2>'+date.toLocaleString('pt-br')+'</h2><ul>';
        for(property in dataR['resources_history_date'][dataI]){//Loop to get updated properties
            let propertyTitle = processPropertyName(property);
            if(property=="INS"){ //loop to get the insertions of a resource
                content+='<li><span style="color:green;">**Resource insertion**</span></li>';
                count+=1;
            }else if(property=="DEL"){//loop to get the removals of a resource
                content+='<li><span style="color:red;">**Resource remotion**</span></li>';
                count+=1;
            }else if(property=="INS_PROP"){
                content+='<li><span style="color:green;">**Relationship insertion**</span></li><ul>';
                dataR['resources_history_date'][dataI][property].forEach(function(att){//loop to get the insertions of a relationship by date
                    let propertyRefTitle = processPropertyName(att[0]);
                    content+='<li><b title="'+att[0]+'">'+propertyRefTitle+'</b>: <span style="color:green;">'+att[1]+'</span></li>';
                    count+=1;
                });
                content+='</ul>';
            }else if(property=="REM_PROP"){
                content+='<li><span style="color:red;">**Relationship remotion**</span></li><ul>';
                dataR['resources_history_date'][dataI][property].forEach(function(att){//loop to get the removals of a relationship by date
                    let propertyRefTitle = processPropertyName(att[0]);
                    content+='<li><b title="'+att[0]+'">'+propertyRefTitle+'</b>: <span style="color:red;">'+att[1]+'</span></li>';
                    count+=1;
                });
                content+='</ul>';
            }
            else{
                content+='<li><b title="'+property+'">'+propertyTitle+'</b></li><ul>';
                dataR['resources_history_date'][dataI][property].forEach(function(att){//loop to get updates for a property
                    content+='<li><span style="color:red;">'+att['previous_value']+'</span> <i class="fa-solid fa-arrow-right"></i> <span style="color:green;">'+att['new_value']+'</span></li>';
                    count+=1;
                });
                content+='</ul>';
            }
        }
        content+='</ul></div>';
        content+='</div>';
    }
    content+='</div>';
    content+='</div>';
    content+='</div>';
    
    
        
    $('#timeline').append(content);
    $('#timeline_filter').append('<option value="timeline_all">All'+' ('+count+')</option>');

    for(property in dataR['resources_history_property']){
        let count = 0;
        let propertyID= property.replaceAll(":","_").replaceAll(",","_").replaceAll("/","_").replaceAll(" ","_").replaceAll(";","").replaceAll("#","").replaceAll(".","_");
        content = '<div id="timeline_'+propertyID+'" class="timeline" style="display:none;">';
        content+='<div class="timeline__wrap">';
        content+='<div class="timeline__items">';
        for(dataI in dataR['resources_history_property'][property]){//Loop para pegar todas as datas para todas as properties
            let date = new Date(dataI);
            content+='<div class="timeline__item">';
            content+='<div class="timeline__content">';
            content+= '<h2>'+date.toLocaleString('pt-br')+'</h2><ul>';
            dataR['resources_history_property'][property][dataI].forEach(function(att){
                content+='<li><span style="color:red;">'+att['previous_value']+'</span> <i class="fa-solid fa-arrow-right"></i> <span style="color:green;">'+att['new_value']+'</span></li>';
                count+=1;
            });
            content+='</ul></div>';
            content+='</div>';
        }
        content+='</div>';
        content+='</div>';
        content+='</div>';
        $('#timeline').append(content);
        $('#timeline_filter').append('<option value="timeline_'+propertyID+'">'+property+' ('+count+')</option>');
    }
    $("#loading").hide();
    timeline(document.querySelectorAll('.timeline'),{
        forceVerticalMode: 600
    });
	return data;
});

function selectTimeline(el){
    $(".timeline").hide();
    $("#"+el.value).show();
}

function processPropertyName(property){
    let split_slash = property.split("/");
    let last_part = (split_slash.length - 1) >= 0 ? (split_slash.length - 1): 0;
    let propertyTitle = split_slash[last_part];
    if(propertyTitle.includes("#")){
        let split_hash = propertyTitle.split("#");
        last_part = (split_hash.length - 1) >= 0 ? (split_hash.length - 1): 0;
        propertyTitle = split_slash[last_part];
    }
    return propertyTitle;
}