let renderTable = {
	
	render: (option) =>{
		
		$(option.el).children().remove();
		
		let cont = `<table class="fater-table">`;
		
		cont = cont + renderTable.renderHead(option.cols);
		
		let request = renderTable.parseParams(option);
		let bodyData = renderTable.getData(request);
		
		if(bodyData.code == 0){

		    if(option.page){

		        if(bodyData.data.data && bodyData.data.data.length > 0){

                    cont = cont + renderTable.renderBody(bodyData.data.data, option.cols);
                    cont = cont + `</table>` ;

                    if(bodyData.data.pageTotal > 1){

                        cont = cont + renderTable.renderPage(bodyData.data.pageIndex, bodyData.data.pageTotal);
                    }
                }else {

                    cont = cont + renderTable.renderEmpty(option.cols.length, "未找到相关内容");
                    cont = cont + `</table>` ;
                }
		    }else{

		        if(bodyData.data && bodyData.data.length > 0){

                    cont = cont + renderTable.renderBody(bodyData.data, option.cols);
                    cont = cont + `</table>` ;
                }else {

                    cont = cont + renderTable.renderEmpty(option.cols.length, "未找到相关内容");
                    cont = cont + `</table>` ;
                }
		    }
		}else{
			
			cont = cont + renderTable.renderError(option.cols.length, bodyData.msg);
			cont = cont + `</table>` ;
		}
		$(option.el).append(cont).show();
		$(".fater-page span").on("click", (e) =>{
			
			if($(e.target).attr("class") != "curr"){
				
				renderTable.handlePage($(e.target).text().trim(), option);
			}
		});

		option.binds();
	},
	renderHead: (cols) =>{
			
		let cont = `<thead><tr>`;
		$.each(cols, (index, item) =>{
			
			cont = cont + `<th>${item.title}</th>`;
		});
		
		cont = cont + `</tr></thead>`;
		
		return cont;
	},
	renderRow: (index, colNumber, colFileds, colTemplates, rowData)=>{
		
		let totalCols = 0;
		
		let cont = `<tr class="fater-table-center">`;
		if(colNumber){
			
			cont = cont + `<td>${index+1}</td>`;
		}
		if(colFileds && colFileds.length > 0){
			
			$.each(colFileds, (index, item) =>{
				
				cont = cont + `<td>${rowData[item]}</td>`;
			});
		}
		if(colTemplates && colTemplates.length > 0){
			
			$.each(colTemplates, (index, item) =>{
				
				cont = cont + `<td>${item(rowData)}</td>`;
			});
		}
		
		cont = cont + `</tr>`;
		
		return cont;
	},
	renderBody: (data, cols)=>{
		
		let cont = `<tbody>`;
		let colNumber = false;
		let colFileds = [];
		let colTemplates = [];
		
		$.each(cols, (index, col) =>{
			
			if(col.type){
				colNumber = true;
			}
			
			if(col.field){
				
				colFileds.push(col.field);
			}
			
			if(col.template){
				
				colTemplates.push(col.template);
			}
		});
		
		$.each(data, (index, item) =>{
			
			cont = cont + renderTable.renderRow(index, colNumber, colFileds, colTemplates, item);
		});
		
		cont = cont + `</tbody>`;
		
		
		return cont;
	},
	renderEmpty: (total, text)=>{
		
		return `<tbody><tr class="fater-table-center"><td colspan="${total}">${text}</td></tr></tbody>`;
	},
	renderError: (total, text)=>{
		
		return `<tbody><tr class="fater-table-center"><td colspan="${total}">${text}</td></tr></tbody>`;
	},
	renderPage: (pageIndex, pageTotal)=>{

		let cont = `<div class="fater-page">`;
		
		for(var i =0; i < pageTotal; i++){
			
			if((i+1) == pageIndex){
				
				cont = cont + `<span class="curr">${i+1}</span>`;
			}else{
				
				cont = cont + `<span>${i+1}</span>`;
			}
		}
		cont = cont + `</div>`;
		
		return cont;
	},
	parseParams(option){
		
		let request = {
			url: "/",
			method: "GET",
			params: null
		};
		
		if(option.url){
			
			request.url = option.url;
		}
		
		if(option.method){
			
			request.method = option.method;
		}
		
		if(option.where){
			
			request.params = option.where;
		}
		
		return request;
	},
	getData: (request)=>{
		var data = {};
		
		$.ajax({
			url: request.url,
			type: request.method,
			async: false,
			data: request.params,
			success: function(res) {
				data = res;
			},
			error: function(res) {
				data = res;
			}
		});
		
		return data;
	},
	handlePage: (pageIndex, option) =>{
		
		option.where["pageIndex"] = pageIndex;
		
		renderTable.render(option);
	}
}

$.extend({
	
	table: (option) =>{
		
		renderTable.render(option);
	}
});