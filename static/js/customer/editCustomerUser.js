layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form
        , layer = layui.layer
        , layedit = layui.layedit
        , laydate = layui.laydate;
    //监听提交
    form.on('submit(save)', function (data) {
        $.ajax({
            type: "put",
            url: "/config/customer/" + data.field.id + '/',
            data: data.field,
            success: function (data, textStatus, xhr) {
                if (xhr.status == 200){
                    layer.msg("修改成功");
                }else {
                    layer.msg("修改失败");
                }
                setTimeout(function () {
                    var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                    parent.layer.close(index); //再执行关闭
                }, 1000);

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
            async: false,//这里设置为同步，异步表格渲染不加载
            dataType: "json",
            success: function (data) {
                for (var i = 0 in data) {
                    $("#group_id").append("<option value=" + data[i].id + ">" + data[i].name + "</option>");
                    renderForm();
                }
            }
        });
    })

});

function inputMemberInfo(data) {
    console.log(data);
    $('input[name="user_account"]').val(data.user_account);
    $("#group_id").val(data.group_id);
    $("#id").val(data.id);
    layui.form.render('select');
}