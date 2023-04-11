const data = d3.json("/query_saved/"+id+"/"+page).then(function(dataR){
	let data = [];
	dataR['vars'].forEach(function(d){
		let row = '<th>';
		row += d;
		row += "</th>";
		$('#elements > thead').append(row);
	});
	$('#elements > thead').append('<th>Grafo</th>');
	dataR['resources'].forEach(function(d){
		let row = '<tr>';
		for(field in d){
			if(field != "graphdb_url")
				row += '<td>'+d[field]+'</td>';	
		}
		row += '<td><a target="_blank" href="'+d.graphdb_url+'">Ver</a></td>';
		row += "</tr>";
		$('#elements > tbody:last-child').append(row);
		data.push(d);
	});
	$("#loading").hide();
	return data;
});


