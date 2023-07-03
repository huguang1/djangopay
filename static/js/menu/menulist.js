layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate'], function () {
    var table = layui.table;
    var laydate = layui.laydate;
    var tableIns = table.render({
        elem: '#menu-table-reload',
        url: window.parent.baseUrl + '/sys/permission',
        method: 'get',
        cols: [[
            {checkbox: true, fixed: 'left'},
            {field: 'id', title: '菜单ID'},
            {field: 'description', title: '菜单名称'},
            {field: 'icon', title: '菜单图标'},
            {field: 'url', title: '菜单地址'},
            {field: 'parent_id', title: '上级菜单ID'},
            {field: 'model_order', title: '菜单排序'},
            {title: '操作', width: 250, align: 'center', fixed: 'right', toolbar: '#menuOpert'}
        ]],
        page: true
        , parseData: function (res) {
            return {
                "code": 0,
                'msg': '',
                "count": res.count,
                "data": res.results
            }
        }
        , limit: 10
        , limits: [5, 10, 100]
        , done: function () {

        }
    });
    //监听工具条
    table.on('tool(menu-table-reload)', function (obj) {
        var data = obj.data;
        if (obj.event === 'editMenu') {
            //编辑
            var index = layer.open({
                title: '修改菜单',
                type: 2,
                content: '/static/view/menu/editmenu.html',
                area: ['600px', '500px'],
                maxmin: true,
                success: function (layero, index) {
                    var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                    var iframeWin = window[layero.find('iframe')[0]['name']];
                    $.ajax({
                        type: 'get',
                        url: window.parent.baseUrl + '/sys/permission/',
                        data: {"all": "all"},
                        success: function (result, textStatus, xhr) {
                            if (xhr.status == 200) {
                                iframeWin.inputDataHandle(result, data);
                            } else {
                                layer.alert('获取失败');
                            }
                        }
                    })
                }
            });
        } else if (obj.event === 'deleteMenu') {
            //删除
            layer.confirm('确认删除该条数据吗？', function (index) {
                $.ajax({
                    type: 'delete',
                    url: window.parent.baseUrl + '/sys/permission/' + data.id + '/',
                    data: {},
                    dataType: 'json',
                    success: function (result, textStatus, xhr) {
                        if (xhr.status == 204) {
                            layer.alert('删除成功', {
                                icon: 6,
                                title: "提示"
                            }, function (index) {
                                layer.close(index);
                                tableIns.reload({
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                            });
                        } else {
                            layer.alert('删除失败', {
                                icon: 5,
                                title: "提示"
                            });
                        }
                    }
                });
            })
        }
    });

    var $ = layui.$, active = {
        getCheckData: function () { //获取选中数据
            var checkStatus = table.checkStatus('menu-table-reload'),
                data = checkStatus.data;
        },
        reload: function () {
            //执行重载
            var menuName = $('#menuName').val();
            table.reload('menu-table-reload', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    key: menuName
                }
            });
        }, add: function () {
            var index = layer.open({
                title: '新增菜单',
                type: 2,
                content: '/static/view/menu/addmenu.html',
                area: ['600px', '500px'],
                maxmin: true,
                success: function (layero, index) {
                    $.ajax({
                        type: 'get',
                        url: window.parent.baseUrl + '/sys/permission/',
                        data: {"all": "all"},
                        success: function (result) {
                            console.log(result);
                            var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                            var iframeWin = window[layero.find('iframe')[0]['name']];
                            iframeWin.inputDataHandle(result);
                        }
                    })
                }
            });
        }
    };
    $('.layui-btn ').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});