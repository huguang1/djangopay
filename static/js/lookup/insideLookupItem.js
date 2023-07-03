layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate', 'jquery'], function () {
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = jQuery = layui.$;
    laydate.render({
        elem: '#loginTime'
        , type: 'datetime'
    });
    var groupCode = g_getQueryString('groupCode');
    var parentGroupCode = g_getQueryString('parentGroupCode');
    var tableIns = table.render({
        elem: '#lookupItem'
        , url: window.parent.baseUrl + '/lookupitem/getLookupItemByGroupCodePage?groupCode=' + groupCode
        , method: 'get'
        , cols: [
            [
                {title: '序号', templet: '#indexTpl', type: 'numbers'}
                , {field: 'itemCode', title: 'item编码'}
                , {field: 'itemName', title: 'item名称'}
                , {field: 'state', title: '状态', templet: '#switchState', unresize: true}
                , {field: 'groupCode', title: '组编码'}
                , {field: 'parentItemCode', title: '父项code'}
                , {field: 'attribute1', title: '属性1'}
                , {field: 'attribute2', title: '属性2'}
                , {field: 'attribute3', title: '属性3'}
                , {field: 'attribute4', title: '属性4'}
                , {field: 'attribute5', title: '属性5'}
                , {fixed: 'right', title: '操作', align: 'center', toolbar: '#toolbar'}
            ]
        ]
        , page: true //是否显示分页
        , limit: 10
        , limits: [5, 10, 100]
        //添加权限控制
        , done: function () {
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

    active = {
        reload: function () {
            // 执行重载
            table.reload('lookupItem', {
                page: {
                    curr: 1
                }
            });
        }
    };

    //监听工具条
    table.on('tool(lookupitemFilter)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
            layer.open({
                type: 2,
                title: false,
                content: '/config/view/lookup/addLookupItem.html?id=' + data.id + '&parentGroupCode=' + parentGroupCode,
                area: ['70%', '90%']
            });
        } else if (obj.event === 'delete') {
            layer.confirm('确认删除？', function (index) {
                $.ajax({
                    type: 'get',
                    url: window.parent.baseUrl + '/lookupitem/deleteById',
                    data: {
                        id: data.id
                    },
                    success: function (data) {
                        if (data > 0) {
                            layer.msg("删除成功");
                        } else {
                            layer.msg("失败");
                        }
                        active.reload();
                    }

                })
                layer.close(index);
            });
        }
    });

    $('#addLookupItem').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/config/view/lookup/addLookupItem.html?groupCode=' + groupCode + '&parentGroupCode=' + parentGroupCode,
            area: ['70%', '90%']
        });
    });
});
