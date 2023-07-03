layui
    .config({
        base: window.parent.baseUrl + '/layui/' //静态资源所在路径
    })
    .use(
        ['table', 'laydate', 'upload', 'element'],
        function () {
            var table = layui.table, upload = layui.upload, jquery = layui.jquery, element = layui.element, form = layui.form
            var tableIns = table.render({
                elem: '#customerList',
                url: window.parent.baseUrl + '/customer',
                method: 'get',
                cols: [[{
                    type: 'checkbox',
                    align: 'center',
                    fixed: 'left'
                }, {
                    field: 'id',
                    title: 'ID',
                    width: '10%',
                    sort: true,
                    align: 'center'
                }, {
                    field: 'user_account',
                    title: '会员账号',
                    align: 'center'
                }, {
                    field: 'group_id',
                    title: '级别编号',
                    align: 'center'
                }, {
                    field: 'group_name',
                    title: '级别名称',
                    align: 'center'
                }, {
                    title: '操作',
                    width: 250,
                    align: 'center',
                    fixed: 'right',
                    toolbar: '#barDemo'
                }]]
                , page: true //是否显示分页
                , parseData: function (res) {
                    return {
                        "code": 0,
                        'msg': '',
                        "count": res.count,
                        "data": res.results
                    }
                }
                , limit: 10,
                limits: [5, 10, 100]
                //添加权限控制
                ,
                done: function () {
                    //查看是否有查询的权限进行按钮控制
                    // if(!checkShiro('add')){
                    //     $("#addbtn").hide();
                    // }
                    // if(!checkShiro('select')){
                    //     $("#selectbtn").hide();
                    // }
                    // if(!checkShiro('delete')){
                    //     $(".del").hide();
                    // }
                    // if(!checkShiro('update')){
                    //     $(".edit").hide();
                    // }
                }
            });

            //监听工具条
            table.on('tool(customerFilter)', function (obj) {
                var data = obj.data;
                if (obj.event === 'del') {
                    layer.confirm('真的删除行么', function (index) {
                        $.ajax({
                            type: "delete",
                            url: "/config/customer/" + data.id + "/",
                            data: {},
                            dataType: "json",
                            success: function (data, textStatus, xhr) {
                                if (xhr.status){
                                    layer.msg("删除成功");
                                }else {
                                    layer.msg("删除失败");
                                }
                                setTimeout(function () {
                                    active.reload();
                                }, 1000);
                            }
                        });
                        layer.close(index);
                    });
                } else if (obj.event === 'edit') {
                    //编辑
                    var index = layer.open({
                        title: '修改会员信息',
                        type: 2,
                        content: '/static/view/customer/editCustomerUser.html',
                        area: ['600px', '570px'],
                        maxmin: true,
                        success: function (layero, index) {
                            var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                            var iframeWin = window[layero.find('iframe')[0]['name']];
                            iframeWin.inputMemberInfo(data);
                        },
                        end: function () {
                            active.reload();
                        }
                    });

                }
            });

            $('.demoTable .layui-btn').on('click', function () {
                var type = $(this).data('type');
                active[type] ? active[type].call(this) : '';
            });
            $('#selectbtn').on('click', function () {
                active.reload();
            });

            $('#batchdel').on('click', function () {
                var checkStatus = table.checkStatus('customerList'), data = checkStatus.data;
                if (data.length == 0) {
                    layer.alert("没有要删除的数据！");
                    return false;
                }
                ;
                var str = new Array;
                for (var i = 0; i < data.length; i++) {
                    str.push(data[i].id);
                }
                layer.confirm('确定删除所选计划吗？', function (index) {
                    $.ajax({
                        type: 'delete',
                        url: '/config/customer/all/',
                        data: {ids: str.join(",")},
                        dataType: 'json',
                        success: function (result, textStatus, xhr) {
                            if (xhr.status == 204) {
                                layer.msg("删除成功");
                                active.reload();
                            } else {
                                layer.alert("删除失败", {
                                    icon: 5,
                                    title: "提示"
                                });
                            }
                        }
                    });
                });
            });
            $('#batchup').on('click', function () {
                var checkStatus = table.checkStatus('customerList'), data = checkStatus.data;
                var customerGroupId = $('#customerGroupId');
                var groupId = customerGroupId.val();
                if (data.length == 0) {
                    layer.alert("没有要更新的数据！");
                    return false;
                }
                ;
                if (!groupId) {
                    layer.alert("请选择批量更新的分层！");
                    return false;
                }
                var str = new Array;
                for (var i = 0; i < data.length; i++) {
                    str.push(data[i].id);
                }
                layer.confirm('确定更新所选计划吗？', function (index) {
                    $.ajax({
                        type: 'get',
                        url: '/config/customer/batchup',
                        data: {
                            ids: str.join(","),
                            groupId: groupId
                        },
                        dataType: 'json',
                        success: function (result) {
                            if (result.success) {
                                layer.msg(result.msg);
                                active.reload();
                            } else {
                                layer.alert(result.msg, {
                                    icon: 5,
                                    title: "提示"
                                });
                            }
                        }
                    });
                });
            });
            active = {
                reload: function () {
                    var customerGroupId = $('#customerGroupId');
                    var userAccount = $('#userAccount');

                    // 执行重载
                    table.reload('customerList', {
                        page: {
                            curr: 1
                        },
                        where: {
                            groupId: customerGroupId.val(),
                            userAccount: userAccount.val()
                        }
                    });
                }
            };
            var token = getCookie("token");
            var opthion = {
                elem: '#test3'
                , url: '/config/customer/upd'
                , accept: 'file' //普通文件
                , data: {}
                , headers: {'X-CSRF-TOKEN': token}
                //,auto: false
                , done: function (res) {
                    if (res.success == true) {
                        layer.msg(res.msg);
                    } else {
                        layer.msg(res.msg);
                    }
                    active.reload();

                }
            };

            form.on('select(pageType)', function (data) {
                var gId = data.value;
                opthion.data.groupId = gId;

            });
            //指定允许上传的文件类型
            upload.render(opthion);

            //重置选择条件
            $('#reset').on('click', function () {
                var groupSelect = document.getElementById("customerGroupId");
                groupSelect.options[0].selected = true;
                $("#userAccount").val("");
                form.render("select");
                active.reload();
            });

        });
$(function () {
    $.ajax({
        type: "GET",
        url: "/config/group/",
        data: {"all": "all"},
        dataType: "json",
        success: function (data) {
            for (var i = 0 in data) {
                if (data[i] && data[i].name) {
                    $("#customerGroupId").append(
                        "<option value=" + data[i].id + ">"
                        + data[i].name + "</option>");
                    renderForm();
                }
            }
        }
    })

});


function renderForm() {
    layui.use('form', function () {
        var form = layui.form;
        form.render();
    });
}
$('#add').on('click', function () {
    layer.open({
        type: 2,
        title: false,
        content: '/static/view/customer/addCustomerInfo.html',
        area: ['35%', '50%']
    });
});
$('#downtemp').on('click', function () {
    window.location.href = "/config/customer/downMemberTemp";
});
