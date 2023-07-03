layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form
        , layer = layui.layer
        , layedit = layui.layedit
        , laydate = layui.laydate;

    //监听提交
    form.on('submit(save)', function (data) {
        console.log(data.field);
        $.ajax({
            type: "post",
            url: "/config/customer/",
            data: data.field,
            success: function (data, textStatus, xhr) {
                if (xhr.status == 201) {
                    layer.msg("添加成功");
                    setTimeout(function () {
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        window.parent.location.reload();
                        parent.layer.close(index); //再执行关闭
                    }, 1000);
                }else {
                    layer.msg("添加失败");
                }
            }
        });
        return false;
    });

    function renderForm() {
        layui.use('form', function () {
            var form = layui.form;
            form.render();
        });
    }

    $(function () {
        $.ajax({
            type: "GET",
            url: "/config/group/",
            data: {"all": "all"},
            dataType: "json",
            success: function (data) {
                for (var i = 0 in data) {
                    $("#group_id").append("<option value=" + data[i].id + ">" + data[i].name + "</option>");
                    renderForm();
                }
            }
        })
    })

});