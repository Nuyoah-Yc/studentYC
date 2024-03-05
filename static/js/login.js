$(function (){

    let checkForm = (loginVal) =>{

        if(!loginVal.userName){

            $.msg("warning", "用户账号必须输入");
            return false;
        }

        if(!loginVal.passWord){

            $.msg("warning", "用户密码必须输入");
            return false;
        }

        return  true;
    };

    $("#loginFormBtn").on("click", (e) =>{

        let loginVal = $.getFrom("loginForm");
        if(checkForm(loginVal)){

            $.ajax({
                url: "/jobs/login/",
                type: "POST",
                data: loginVal,
                success: function(res){
                    if(res.code == 0){
                    	
                    	window.location.href="/jobs/show/";
                    }else{
                        $.msg("error", res.msg);
                    }
                }
            });
        }
    });
});