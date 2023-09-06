
const data = d3.json("/query_saved/"+id+"/"+page+filters).then(function(dataR){
	let data = [];
	dataR['vars'].forEach(function(d){
		let row = '<th>';
		row += d;
		row += "</th>";
		$('#elements > thead').append(row);
	});
	$('#elements > thead').append('<th>Graph</th>');
	dataR['resources'].forEach(function(d){
		let row = '<tr>';
		for(field in d){
			if(field != "graphdb_url")
				if(d[field].includes('http://') || d[field].includes('https://'))
					row += '<td><a href="/browser?uri='+d[field]+'">'+d[field]+"</a></td>";
				else
					row += '<td>'+d[field]+'</td>';	
		}
		row += '<td><a target="_blank" href="'+d.graphdb_url+'">View</a></td>';
		row += "</tr>";
		$('#elements > tbody:last-child').append(row);
		data.push(d);
	});
	$("#loading").hide();
	return data;
});


