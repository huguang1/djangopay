var $ = layui.$;
layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['form', 'laydate'], function () {
    layer = layui.layer,
        form = layui.form,
        index = parent.layer.getFrameIndex(window.name); //获取窗口索引;
    /* 自定义验证规则 */
    form.verify({
        userName: function (value) {
            if (value.length < 5) {
                return '名称至少得5个字';
            }
        }
    });

    $(function () {
        $("#btnEditRoleSubmit").click(function () {
            var role_name = $("#role_name").val();
            var role_desc = $("#role_desc").val();
            if (!role_name || !role_desc) {
                layer.alert("角色名字或者描述不能为空");
                return;
            }
            var data = $("#myForm").serialize();
            $.ajax({
                type: 'post',
                url: window.parent.parent.baseUrl + '/sys/role/',
                data: data,
                dataType: 'json',
                success: function (result, textStatus, xhr) {
                    if (xhr.status == 201) {
                        layer.alert("新增成功", {
                            icon: 6,
                            title: "提示"
                        }, function (index) {
                            layer.close(index);
                            var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                            parent.layer.close(index); //再执行关闭
                            window.parent.location.reload();
                        });
                    } else {
                        layer.alert("新增失败", {
                            icon: 5,
                            title: "提示"
                        }, function (index) {
                            layer.close(index);
                            var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                            parent.layer.close(index); //再执行关闭
                            window.parent.location.reload();
                        });
                    }
                }
            });
        })
        //取消按钮监听
        $("#btnCancel").click(function () {
            parent.layer.close(index);
        })
    })
});


