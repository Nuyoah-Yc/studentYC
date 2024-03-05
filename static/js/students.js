function handle(){

	$("button[event=upd]").on("click", (e)=>{

        $.ajax({
            url: "/jobs/students/info/",
            type: "GET",
            async: false,
            data:{
                id: $(e.target).attr("data"),
            },
            success: function(res){
                if(res.code == 0){

                    $.initForm("updForm", res.data);
                    $.model(".updWin");
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });

    $("button[event=del]").on("click", (e)=>{

        $.confirm("确认要删除吗", () =>{

            $.ajax({
                url: "/jobs/students/del/",
                type: "POST",
                async: false,
                data:{
                    id: $(e.target).attr("data"),
                },
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
    });
}

$(function (){

    let tableView =  {
        el: "#tableShow",
        url: "/jobs/students/page/",
        method: "GET",
        where: {
            pageIndex: 1,
            pageSize: 10
        },
        page: true,
        cols: [
			{
				field: "id",
				title: "学生学号",
				align: "center",
			},
			{
				field: "userName",
				title: "学生账号",
				align: "center",
			},
			{
				field: "name",
				title: "学生姓名",
				align: "center",
			},
			{
				field: "gender",
				title: "学生性别",
				align: "center",
			},
			{
				field: "age",
				title: "学生年龄",
				align: "center",
			},
			{
				field: "phone",
				title: "学生电话",
				align: "center",
			},
			{
				field: "address",
				title: "联系电话",
				align: "center",
			},
			{
				field: "birthday",
				title: "出生日期",
				align: "center",
			},
			{
				field: "collegeName",
				title: "所属学院",
				align: "center",
			},
			{
				field: "majorName",
				title: "所学专业",
				align: "center",
			},
			{
				title: "学生状态",
				align: "center",
				template: (d)=>{

				    return d.status == 0 ? '待业' : '就业'
				}
			},
			{
                title: "操作",
                template: (d)=>{

                    return `
                            <button type="button" event="upd" data="${d.id}" class="fater-btn fater-btn-primary fater-btn-sm">
                                <span data="${d.id}" class="fa fa-edit"></span>
                            </button>
                            <button type="button" event="del" data="${d.id}" class="fater-btn fater-btn-danger fater-btn-sm">
                                <span data="${d.id}" class="fa fa-trash"></span>
                            </button>
                            `;
                }
            }
        ],
        binds: (d) =>{

            handle();
        }
    }
    $.table(tableView);

    $(".fater-btn-form-qry").on("click", ()=>{

        tableView.where["userName"] = $("[name=para1]").val();
        tableView.where["name"] = $("[name=para2]").val();
        tableView.where["phone"] = $("[name=para3]").val();
        tableView.where["collegeId"] = $("[name=para4]").val();
        tableView.where["majorId"] = $("[name=para5]").val();

        $.table(tableView);
    });

    $("button[event=add]").on("click", ()=>{

        $.model(".addWin");
    });

    $("#addFormBtn").on("click", ()=>{

        let formVal = $.getFrom("addForm");

        $.ajax({
            url: "/jobs/students/add/",
            type: "POST",
            data: formVal,
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

    $("#updFormBtn").on("click", ()=>{

        let formVal = $.getFrom("updForm");

        $.ajax({
            url: "/jobs/students/upd/",
            type: "POST",
            data: formVal,
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
});