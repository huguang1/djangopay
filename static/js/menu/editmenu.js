//重新渲染表单
var $ = layui.$;
function renderForm() {
    layui.use('form', function () {
        var form = layui.form;//高版本建议把括号去掉，有的低版本，需要加()
        form.render();
    });
};

function inputDataHandle(parenMenu, data) {
    $("#id").val(data.id);
    $("#description").val(data.description);
    $("#url").val(data.url);
    $("#parent_id").val(data.parent_id);
    $("#model_order").val(data.model_order);
    $("#icon").val(data.icon);
    //动态加载下拉框
    var objSelect = document.getElementById("parent_id");
    for (var i = 0; i < parenMenu.length; i++) {
        objSelect.options.add(new Option(parenMenu[i].description, parenMenu[i].id));
    }
    renderForm();
    var select = 'dd[lay-value=' + data.parent_id + ']';
    $('#parent_id').siblings("div.layui-form-select").find('dl').find(select).click();
}

layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['form', 'laydate'], function () {
    layer = layui.layer,
        form = layui.form,
        index = parent.layer.getFrameIndex(window.name); //获取窗口索引;
    /* 监听提交 */
    form.on('submit(editMenuSubmit)', function (data) {
        console.log(data.field);
        $.ajax({
            type: 'put',
            url: window.parent.parent.baseUrl + '/sys/permission/' + data.field.id + '/',
            data: data.field,
            success: function (result, textStatus, xhr) {
                if (xhr.status == 200) {
                    layer.alert("编辑成功", {
                        icon: 6,
                        title: "提示"
                    }, function (index) {
                        layer.close(index);
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                        window.parent.location.reload();
                    });
                } else {
                    layer.alert("编辑失败", {
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
        })
        return false;
    });

    var active = {
        cancel: function (set) {
            parent.layer.close(index);
        }
    }
    $('.layui-btn').on('click', function () {
        var othis = $(this),
            type = othis.data('type');
        active[type] && active[type].call(this);
    });

});