layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form
        , layer = layui.layer
        , layedit = layui.layedit
        , laydate = layui.laydate;

    var token = getCookie("token");
    //监听提交
    form.on('submit(save)', function (data) {
        console.log(data.field);
        console.log();
        $.ajax({
            type: "put",
            url: "/config/dictionary/" + data.field.id + "/",
            data: data.field,
            headers: {'X-CSRF-TOKEN': token},
            success: function (data, textStatus, xhr) {
                if (xhr.status == 200) {
                    layer.msg("修改成功");
                    setTimeout(function () {
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                    }, 1000);

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
});

function inputMemberInfo(data) {
    $('input[name="dic_key"]').val(data.dic_key);
    $('input[name="dic_value"]').val(data.dic_value);
    $('input[name="description"]').val(data.description);
    $("#id").val(data.id);
    layui.form.render('select');
}
