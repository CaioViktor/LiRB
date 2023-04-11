const data = d3.json("/classes").then(function(dataR){
	dataR['classes'].forEach(function(d){
		let item ='<div class="card" style="width: 18rem;">	<div class="card-body"><h5 class="card-title">'+d['label']+'</h5><h6 class="card-subtitle mb-2 text-muted"><a href="resources/0?classRDF='+d.uri+'&label='+d.label+'">'+d['uri_raw']+'</a></h6><p class="card-text text-truncate-meu tooltip1">'+d['comment']+'<span class="tooltip1text">'+d['comment']+'</span></p>';
		if(d['subclasses'].length > 0){
			item+= '<hr/><h7>Sub-Tipos:</h7><ul class="list-group list-group-flush">';
			d.subclasses.forEach(function(subclass){
				item+='<li class="list-group-item"><a href="resources/0?classRDF='+subclass[0]+'&label='+subclass[1]+'" title="'+subclass[0]+'" target="_blank">'+subclass[1]+'</li>';
			})
			item+= '</ul>';
		}
		item+= '<a href="resources/0?classRDF='+d.uri+'&label='+d.label+'" class="btn btn-primary">Explorar</a>	</div> </div>';
		$('#list_classes').append(item);
	});
	dataR['classes_destaque'].forEach(function(d){
		let item ='<div class="card" style="width: 18rem;">	<div class="card-body"><h5 class="card-title">'+d['label']+'</h5><h6 class="card-subtitle mb-2 text-muted"><a href="resources/0?classRDF='+d.uri+'&label='+d.label+'">'+d['uri_raw']+'</a></h6><p class="card-text text-truncate-meu tooltip1">'+d['comment']+'<span class="tooltip1text">'+d['comment']+'</span></p>';
		if(d['subclasses'].length > 0){
			item+= '<hr/><h7>Sub-Tipos:</h7><ul class="list-group list-group-flush">';
			d.subclasses.forEach(function(subclass){
				item+='<li class="list-group-item"><a href="resources/0?classRDF='+subclass[0]+'&label='+subclass[1]+'" title="'+subclass[0]+'" target="_blank">'+subclass[1]+'</li>';
			})
			item+= '</ul>';
		}
		item+= '<a href="resources/0?classRDF='+d.uri+'&label='+d.label+'" class="btn btn-primary">Explorar</a>	</div> </div>';
		$('#list_classes_destaque').append(item);
	});
	$("#loading").hide()
	$("#loading_destaque").hide()
	
	return dataR;
});
$(function () {
	$('[data-toggle="tooltip"]').tooltip()
  })