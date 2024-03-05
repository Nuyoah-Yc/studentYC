$(function (){

    $(".fater-user").on("click", (e) =>{

        $(e.target).find(".fater-user-list").toggleClass(" fater-user-show");
    });

    $("#sessionInfo").on("click", () =>{

        $.ajax({
            url: "/jobs/info/",
            type: "GET",
            async: false,
            success: function(res){
                if(res.code == 0){

                    $.initForm("updSessionInfoForm", res.data);
                    $.model(".updSessionInfoWin");
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });

    $("#updSessionInfoFormBtn").on("click", () =>{

        let formVal = $.getFrom("updSessionInfoForm");
        $.ajax({
            url: "/jobs/info/",
            type: "POST",
            data: formVal,
            async: false,
            success: function(res){
                if(res.code == 0){

                    $.alert(res.msg, () =>{

                        window.location.reload();
                    });
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });

    $("#sessionPwd").on("click", () =>{

        $.ajax({
            url: "/jobs/info/",
            type: "GET",
            async: false,
            success: function(res){
                if(res.code == 0){

                    $.initForm("updSessionPwdForm", {id: res.data.id, passWord:  res.data.passWord});
                    $.model(".updSessionPwdWin");
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });

    let checkForm = (formVal) =>{

        if(!formVal.oldPwd){

            $.msg("warning", "原始密码必须输入");
            return false;
        }

        if(formVal.oldPwd && formVal.oldPwd != formVal.passWord){

            $.msg("warning", "原始密码输入错误");
            return false;
        }

        if(!formVal.newPwd){

            $.msg("warning", "修改密码必须输入");
            return false;
        }

        if(!formVal.repPwd){

            $.msg("warning", "确认密码必须输入");
            return false;
        }

        if(formVal.repPwd && formVal.repPwd != formVal.newPwd){

            $.msg("warning", "两次输入的密码不一致");
            return false;
        }

        return true;
    };

    $("#updSessionPwdFormBtn").on("click", () =>{

        let formVal = $.getFrom("updSessionPwdForm");

        if(checkForm(formVal)){

            $.ajax({
                url: "/jobs/pwd/",
                type: "POST",
                data: {
                    password: formVal.newPwd
                },
                async: false,
                success: function(res){
                    if(res.code == 0){

                        $.alert(res.msg, () =>{

                            window.location.reload();
                        });
                    }else{
                        $.msg("error", res.msg);
                    }
                }
            });
        }
    });

    $("#sessionExit").on("click", () =>{

        $.confirm("确认要退出吗？", () =>{

            window.location.href="/jobs/exit/";
        });
    });
});