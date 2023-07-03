function GetRequest() {
    var url = location.search;
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}

layui.use(['form', 'layedit', 'laydate', 'jquery'],
    function () {
        var form = layui.form, layer = layui.layer, layedit = layui.layedit, laydate = layui.laydate;
        var $ = layui.jquery;

        // 自定义验证规则
        form.verify({});

        // 监听提交
        form.on('submit(mainSub)', function (data) {
            if (data.field.state == "on") {
                data.field.state = "1";
            } else {
                data.field.state = "0";
            }
            if (!data.field.min_switch) {
                data.field.min_switch = "off";
            }
            if (!data.field.max_switch) {
                data.field.max_switch = "off"
            }
            if (!data.field.point_switch) {
                data.field.point_switch = "off"
            }
            var token = getCookie("token");
            $.ajax({
                type: "post",
                url: "/config/payinfo/",
                data: data.field,
                headers: {'X-CSRF-TOKEN': token},
                dataType: "json",
                success: function (obj, textStatus, xhr) {
                    if (xhr.status == 200 || xhr.status == 201) {
                        layer.msg("保存成功！");
                        setTimeout(function () {
                            var index = parent.layer.getFrameIndex(window.name);
                            parent.layer.close(index);
                        }, 1000);
                    } else {
                        layer.msg("保存失败");
                    }
                }
            });
            return false;
        });

        // 初始化数据
        $(function () {
            var Request = GetRequest();
            var infoId = Request['id'];
            $.ajax({
                type: 'get',
                url: '/config/lookupitem/?group_code=PAY_TYPE&state=1',
                data: {"all": "all"},
                async: false,
                success: function (result) {
                    //动态加载下拉框
                    var objSelect = document.getElementById("item_code");
                    var data = result;
                    for (var i = 0; i < data.length; i++) {
                        objSelect.options.add(new Option(data[i].item_name, data[i].item_code));
                    }
                    renderForm();
                }
            })
            $.ajax({
                type: 'get',
                url: '/config/payapi/',
                async: false,
                data: {"all": "all"},
                success: function (result) {
                    //动态加载下拉框
                    var objSelect = document.getElementById("payment_code");
                    var data = result;
                    for (var i = 0; i < data.length; i++) {
                        objSelect.options.add(new Option(data[i].payment_name, data[i].payment_code));
                    }
                    renderForm();
                }
            })
            $.ajax({
                type: 'get',
                url: '/config/lookupitem/?group_code=BANK_GROUP&state=1',
                data: {"all": "all"},
                async: false,
                success: function (result) {
                    //动态加载下拉框
                    var objSelect = document.getElementById("bank_code");
                    var data = result;
                    for (var i = 0; i < data.length; i++) {
                        objSelect.options.add(new Option(data[i].item_name, data[i].item_code));
                    }
                    renderForm();
                }
            })

            if (typeof(infoId) != "undefined") {
                $.ajax({
                    type: "get",
                    url: "/config/payinfo/",
                    async: false,
                    data: {
                        id: infoId
                    },
                    success: function (result) {
                        var obj = result[0];
                        form.val('mainForm', obj);
                        if (obj.minSwitch == 'off') {
                            var a = document.getElementById("min_switch");
                            a.checked = false;
                        }
                        if (obj.pointSwitch == 'off') {
                            var b = document.getElementById("max_switch");
                            b.checked = false;
                        }
                        if (obj.pointSwitch == 'off') {
                            var c = document.getElementById("point_switch");
                            c.checked = false;
                        }
                        if (!obj.itemCode || obj.itemCode == '' || obj.itemCode != 'CYBER_BANK') {
                            document.getElementById('wangyinTypeDiv').style.display = 'none';
                            document.getElementById('bankCategoryDiv').style.display = 'none';
                        } else {
                            $("#wangyin_type option[value=" + obj.pay_model + "]").prop("selected", true);
                            form.render("select");
                            if (obj.payModel == '3') {
                                $("#remark option[value=" + obj.remark + "]").prop("selected", true);
                            } else {
                                document.getElementById('bankCategoryDiv').style.display = 'none';
                            }
                        }
                        form.render();
                    }
                });

            } else {
                document.getElementById('wangyinTypeDiv').style.display = 'none';
                document.getElementById('bankCategoryDiv').style.display = 'none';
            }
        });

        form.on('select(payTypeFilter)', function (data) {
            if ($('#itemCode').val() == 'CYBER_BANK') {
                document.getElementById('wangyinTypeDiv').style.display = 'block';
                document.getElementById('bankCategoryDiv').style.display = 'block';
            } else {
                document.getElementById('wangyinTypeDiv').style.display = 'none';
                document.getElementById('bankCategoryDiv').style.display = 'none';
            }
        });

        form.on('select(wangyinTypeFilter)', function (data) {
            if ($('#wangyinType').val() == '3') {
                document.getElementById('bankCategoryDiv').style.display = 'block';
            } else {
                document.getElementById('bankCategoryDiv').style.display = 'none';
            }
        });

        form.on('select(rateTypeFilter)', function (data) {
            document.getElementById('rate').value = "";
        });

    });
function getCookie(sName) {
    var aCookie = document.cookie.split("; ");
    for (var i = 0; i < aCookie.length; i++) {
        var aCrumb = aCookie[i].split("=");
        if (sName == aCrumb[0])
            return unescape(aCrumb[1]);
    }
    return null;
}