let msgWin = {
	
	success: (msg) =>{
		
		let content = `
					<div class="fater-model-msg fater-model-msg-success">
						<span class="fa fa-check-square"></span> ${msg}
					</div>
					`;
		$("body").append(content).show();
		$(".fater-model-msg").fadeOut(3000, () =>{
		
			$(".fater-model-msg").remove();
		});
	},
	warning: (msg) =>{
		
		let content = `
					<div class="fater-model-msg fater-model-msg-warning">
						<span class="fa fa-exclamation-triangle"></span> ${msg}
					</div>
					`;
		$("body").append(content).show();
		$(".fater-model-msg").fadeOut(3000, () =>{
		
			$(".fater-model-msg").remove();
		});
	},
	error: (msg) =>{
		
		let content = `
					<div class="fater-model-msg fater-model-msg-error">
						<span class="fa fa-times-circle"></span> ${msg}
					</div>
					`;
		$("body").append(content).show();
		$(".fater-model-msg").fadeOut(3000, () =>{
		
			$(".fater-model-msg").remove();
		});
	},
	info: (msg) =>{
		
		let content = `
					<div class="fater-model-msg fater-model-msg-info">
						<span class="fa fa-info-circle"></span> ${msg}
					</div>
					`;
		$("body").append(content).show();
		$(".fater-model-msg").fadeOut(3000, () =>{
		
			$(".fater-model-msg").remove();
		});
	},
};

let alertWin = (msg, fn) =>{
	
	let content = `
				<div class="fater-model-alert">
					<div class="fater-model-alert-head">
						<span>系统提示</span>
						<span>×</span>
					</div>
					<div class="fater-model-alert-body">
						<div class="fater-model-alert-msg">
							${msg}
						</div>
						<div class="fater-model-alert-btns">
							<button event="ok" type="button" class="fater-btn fater-btn-primary fater-btn-sm">
								知道啦
							</button>
						</div>
					</div>
				</div>
				`;
				
	$("body").append(content).show();
	
	$("button[event='ok']").on("click", fn);
	
	$(".fater-model-alert-head span:last-child").on("click", () =>{
		
		$(".fater-model-alert").remove();
	});
};

let confirmWin = (msg, fn) =>{
	
	let content = `
				<div class="fater-model-alert">
					<div class="fater-model-alert-head">
						<span>系统提示</span>
						<span>×</span>
					</div>
					<div class="fater-model-alert-body">
						<div class="fater-model-alert-msg">
							${msg}
						</div>
						<div class="fater-model-alert-btns">
							<button event="ok" type="button" class="fater-btn fater-btn-primary fater-btn-sm">
								确认
							</button>
							<button event="cancel" type="button" class="fater-btn fater-btn-normal fater-btn-sm">
								取消
							</button>
						</div>
					</div>
				</div>
				`;
				
	$("body").append(content).show();
	
	$("button[event='ok']").on("click", fn);
	
	$("button[event='cancel']").on("click", () =>{
		
		$(".fater-model-alert").remove();
	});
	
	$(".fater-model-alert-head span:last-child").on("click", () =>{
		
		$(".fater-model-alert").remove();
	});
};

let modelmWin = (el) =>{

	$(el).removeClass("fater-model-hidden");
	$(".fater-model-win-head span:last-child").on("click", () =>{

		$(el).addClass("fater-model-hidden");
	});
};

$.extend({
    msg: (type, msg) =>{
		
		if(type == "success"){
			
			msgWin.success(msg);
		}else if(type == "warning"){
			
			msgWin.warning(msg);
		}else if(type == "error"){
			
			msgWin.error(msg);
		}else{
			
			msgWin.info(msg);
		}
	},
	alert: (msg, fn) =>{
		
		alertWin(msg, fn);
	},
	confirm: (msg, fn) =>{
		
		confirmWin(msg, fn);
	},
	model: (el) =>{
		
		modelmWin(el);
	}
})