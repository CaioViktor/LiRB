const data = d3.json("/list_resources/"+page+"?classRDF="+classRDF+"&search="+search).then(function(dataR){
	let data = [];
	dataR.forEach(function(d){
		
		let row = '<tr>';
		// row += '<td title="'+d.graphdb_url+'"><li><a target="_blank" href="'+d.graphdb_url+'">'+d.label+"</a></li></td>";
		row += '<td><li><a target="_blank" href="/browser?uri='+d.uri+'">'+d.label+"</a></li></td>";
		row += "</tr>";
		$('#elements > tbody:last-child').append(row);
		data.push(d);
	});
	$("#loading").hide();
	return data;
});


