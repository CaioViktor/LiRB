const propriedadesDestaque = ['http://www.w3.org/2000/01/rdf-schema#label','http://www.w3.org/1999/02/22-rdf-syntax-ns#type','http://www.w3.org/2000/01/rdf-schema#comment','http://dbpedia.org/ontology/thumbnail','http://xmlns.com/foaf/0.1/thumbnail','http://xmlns.com/foaf/0.1/img','http://www.sefaz.ma.gov.br/ontology/tem_timeLine'];
let propriedades_list = null;
let classes_list = null;
const label = d3.json("/get_label?uri="+encodeURI(uri)).then(function(dataR){
    $("#label_resource")[0].innerHTML=": <b><i>" +dataR.label+"</i></b>";
    return dataR.label
});
const data = d3.json("/get_historico?uri="+encodeURI(uri)).then(function(dataR){
	let data = dataR;
    
    let count = 0;
    let content = '<div id="timeline_all" class="timeline">';//Timeline todas as propriedades
    content+='<div class="timeline__wrap">';
    content+='<div class="timeline__items">';
    for(dataI in dataR['resources_historico_data']){//Loop para pegar todas as datas para todas as propriedades
        let date = new Date(dataI);
        content+='<div class="timeline__item">';
        content+='<div class="timeline__content">';
        content+= '<h2>'+date.toLocaleString('pt-br')+'</h2><ul>';
        for(propriedade in dataR['resources_historico_data'][dataI]){//Loop pára pegar as propriedades atualizadas
            let propriedadeTitle = propriedade.replaceAll("/",' / ');
            if(propriedade=="INS"){
                content+='<li><span style="color:green;">**INSERÇÃO DE INSTÂNCIA**</span></li>';
                count+=1;
            }else if(propriedade=="DEL"){
                content+='<li><span style="color:red;">**REMOÇÃO DE INSTÂNCIA**</span></li>';
                count+=1;
            }else if(propriedade=="INS_PROP"){
                content+='<li><span style="color:green;">**INSERÇÃO DE RELACIONAMENTO**</span></li><ul>';
                dataR['resources_historico_data'][dataI][propriedade].forEach(function(att){//loop para pegar as atualizações para uma propriedade em uma data
                    content+='<li><b>'+att[0]+'</b>: <span style="color:green;">'+att[1]+'</span></li>';
                    count+=1;
                });
                content+='</ul>';
            }else if(propriedade=="REM_PROP"){
                content+='<li><span style="color:red;">**REMOÇÃO DE RELACIONAMENTO**</span></li><ul>';
                dataR['resources_historico_data'][dataI][propriedade].forEach(function(att){//loop para pegar as atualizações para uma propriedade em uma data
                    content+='<li><b>'+att[0]+'</b>: <span style="color:red;">'+att[1]+'</span></li>';
                    count+=1;
                });
                content+='</ul>';
            }
            else{
                content+='<li><b>'+propriedadeTitle+'</b></li><ul>';
                dataR['resources_historico_data'][dataI][propriedade].forEach(function(att){//loop para pegar as atualizações para uma propriedade em uma data
                    content+='<li><span style="color:red;">'+att['valor_antigo']+'</span> <i class="fa-solid fa-arrow-right"></i> <span style="color:green;">'+att['valor_novo']+'</span></li>';
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
    $('#timeline_filter').append('<option value="timeline_all">Todos'+' ('+count+')</option>');

    for(propriedade in dataR['resources_historico_propriedade']){
        let count = 0;
        let propriedadeID= propriedade.replaceAll(":","_").replaceAll(",","_").replaceAll("/","_").replaceAll(" ","_").replaceAll(";","");
        content = '<div id="timeline_'+propriedadeID+'" class="timeline" style="display:none;">';
        content+='<div class="timeline__wrap">';
        content+='<div class="timeline__items">';
        for(dataI in dataR['resources_historico_propriedade'][propriedade]){//Loop para pegar todas as datas para todas as propriedades
            let date = new Date(dataI);
            content+='<div class="timeline__item">';
            content+='<div class="timeline__content">';
            content+= '<h2>'+date.toLocaleString('pt-br')+'</h2><ul>';
           
            dataR['resources_historico_propriedade'][propriedade][dataI].forEach(function(att){
                content+='<li><span style="color:red;">'+att['valor_antigo']+'</span> <i class="fa-solid fa-arrow-right"></i> <span style="color:green;">'+att['valor_novo']+'</span></li>';
                count+=1;
            });
            content+='</ul></div>';
            content+='</div>';
        }
        content+='</div>';
        content+='</div>';
        content+='</div>';
        $('#timeline').append(content);
        $('#timeline_filter').append('<option value="timeline_'+propriedadeID+'">'+propriedade+' ('+count+')</option>');
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

