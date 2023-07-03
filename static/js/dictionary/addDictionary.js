layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form
        , layer = layui.layer
        , layedit = layui.layedit
        , laydate = layui.laydate;
    var token = getCookie("token");
    //监听提交
    form.on('submit(save)', function (data) {
        $.ajax({
            type: "post",
            url: "/config/dictionary/",
            data: data.field,
            headers: {'X-CSRF-TOKEN': token},
            success: function (data, textStatus, xhr) {
                if (xhr.status == 201) {
                    layer.msg('创建成功');
                    setTimeout(function () {
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        window.parent.location.reload();
                        parent.layer.close(index); //再执行关闭
                    }, 1000);
                }
            }
        });
        return false;
    });
});