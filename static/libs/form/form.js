let setFromVals = (form, vals) =>{
	
	let formBody= $("form[name=" + form + "]");
	
	let el_text = $("form[name=" + form + "]").find("input[type=text]");
	let el_pwd = $("form[name=" + form + "]").find("input[type=password]");
	let el_radio = $("form[name=" + form + "]").find("input[type=radio]");
	let el_checkbox = $("form[name=" + form + "]").find("input[type=checkbox]");
	let el_hidden = $("form[name=" + form + "]").find("input[type=hidden]");
	let el_select = $("form[name=" + form + "]").find("select");
	let el_textarea = $("form[name=" + form + "]").find("textarea");
	
	$.each(Object.keys(vals), (index, item) =>{
		$.each(el_text, (i, e) =>{
			
			if ($(e).attr("name") == item) {
				$(e).attr("value", vals[item]);
			}
		});
		
		$.each(el_pwd, (i, e) =>{
			
			if ($(e).attr("name") == item) {
				$(e).attr("value", vals[item]);
			}
		});
		
		$.each(el_radio, (i, e) =>{
			
			if ($(e).attr("name") == item && $(e).attr("value") == vals[item]) {
				$(e).attr("checked", "true");
			}
		});
		
		$.each(el_checkbox, (i, e) =>{
			
			if ($(e).attr("name") == item && $(e).attr("value") == vals[item]) {
				$(e).attr("checked", "true");
			}
		});
		
		$.each(el_hidden, (i, e) =>{
			
			if ($(e).attr("name") == item) {
				$(e).val(vals[item]);
			}
		});
		
		$.each(el_select, (i, e) =>{
			
			if ($(e).attr("name") == item) {
				$(e).val(vals[item]);
			}
		});
		
		$.each(el_textarea, (i, e) =>{
			
			if ($(e).attr("name") == item) {
				$(e).text(vals[item]);
			}
		});
		
	});
};

let getFormVals = (form) =>{
	
	let formBody= $("form[name=" + form + "]");
	
	let formVal = {};
	let el_text = $("form[name=" + form + "]").find("input[type=text]");
	let el_pwd = $("form[name=" + form + "]").find("input[type=password]");
	let el_radio = $("form[name=" + form + "]").find("input[type=radio]");
	let el_checkbox = $("form[name=" + form + "]").find("input[type=checkbox]");
	let el_hidden = $("form[name=" + form + "]").find("input[type=hidden]");
	let el_select = $("form[name=" + form + "]").find("select");
	let el_textarea = $("form[name=" + form + "]").find("textarea");
	
	$.each(el_text, (index, item) =>{
				
		formVal[$(item).attr("name")] = $(item).val();
	});
	
	$.each(el_pwd, (index, item) =>{
		
		formVal[$(item).attr("name")] = $(item).val();
	});
	
	$.each(el_radio, (index, item) =>{
		
		formVal[$(item).attr("name")] = $("input[name="+ $(item).attr("name") +"]:checked").val();
	});
	
	// $.each(el_checkbox, (index, item) =>{
		
	// 	formVal[$(item).attr("name")].push($("input[name="+ $(item).attr("name") +"]:checked").val());
	// });
	
	$.each(el_hidden, (index, item) =>{
		
		formVal[$(item).attr("name")] = $(item).val();
	});
	
	$.each(el_select, (index, item) =>{
		
		formVal[$(item).attr("name")] = $(item).val();
	});
	
	$.each(el_textarea, (index, item) =>{
		
		formVal[$(item).attr("name")] = $(item).val().trim();
	});
	
	
	return formVal;
};

let checkFormVals = (form) =>{
	
};

$.extend({
	initForm: (form, vals) =>{
		
		setFromVals(form, vals);
	},
	getFrom: (form) =>{
		
		return getFormVals(form);
	},
	checkForm: (form) =>{
		
	}
});