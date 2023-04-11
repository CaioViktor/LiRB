// const classes = d3.json("/classes").then(function(dataR){
// 	let data = dataR;
//     let options = '<option value="null">--SELECIONAR--</option>';
// 	dataR.forEach(function(d){
//         options +='<option value="'+d.uri+'">'+d.label+'</option>';
//     });
//     $("#classe").html(options)
// 	return data;
// });

function main(uri){
    historico = d3.json("/get_historico?uri="+uri).then(function(dataR){
        let options = '<option value="null">--SELECIONAR--</option>';
        
        for(propriedade in(dataR['resources_historico_propriedade'])){
            options +='<option value="'+propriedade+'">'+propriedade+'</option>';
        }
        $("#atributo").html(options)
        dataHistorico = structuredClone(dataR);
        return dataR;
    });
    return historico;
}

let atributos = [];

$('#atributo').on('change', function() {
    let propriedade = this.value;    
    let options = '<option value="null">--SELECIONAR--</option>';
    for(date in dataHistorico['resources_historico_propriedade'][propriedade]){
        options +='<option value="'+date+'">'+date+'</option>';
    }
    $("#data").html(options);

  });

$('#data').on('change', function() {
    let data = this.value;    
    propriedade = $("#atributo")[0].value;
    let tabela = '<thead><th>Valor Antigo</th><th>Valor Novo</th></thead><tbody>\n';
    dataHistorico['resources_historico_propriedade'][propriedade][data].forEach(element => {
        tabela+= '<tr><td>'+element['valor_antigo']+'</td><td>'+element['valor_novo']+'</td></tr>';
    });
    tabela+='</tbody>';
    $("#elements").html(tabela);

  });