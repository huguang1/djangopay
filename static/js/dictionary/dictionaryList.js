layui.use(['table', 'layer',], function () {
    var $ = layui.jquery, layer = layui.layer;
    var table = layui.table;
    var tableIns = table.render({
        elem: '#dictionaryList',
        url: window.parent.baseUrl + '/dictionary',
        method: 'get',
        cols: [[{
            field: 'id',
            title: 'ID',
            sort: true,
            align: 'center'
        }, {
            field: 'dic_key',
            title: '字典key',
            align: 'center'
        }, {
            field: 'dic_value',
            title: '字典值',
            align: 'center'
        }, {
            field: 'description',
            title: '字典描述',
            align: 'center'
        }, {
            title: '操作',
            width: 250,
            align: 'center',
            fixed: 'right',
            toolbar: '#barDemo'
        }]],
        page: true // 是否显示分页
        , parseData: function (res) {
            return {
                "code": 0,
                'msg': '',
                "count": res.count,
                "data": res.results
            }
        }
        , limit: 10,
        limits: [10, 100]
        // 添加权限控制
    });

    $('#selectbtn').on('click', function () {
        active.reload();
    });
    // 监听工具条
    table.on('tool(demo)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.confirm('真的删除行么', function (index) {
                $.ajax({
                    type: "delete",
                    url: "/config/dictionary/" + data.id + "/",
                    data: {},
                    dataType: "json",
                    success: function (data, textStatus, xhr) {
                        if (xhr.status == 204){
                            layer.msg('删除成功');
                            setTimeout(function () {
                                active.reload();
                            }, 1000);
                        }
                    }
                });
                layer.close(index);
            });
        } else if (obj.event === 'edit') {
            var index = layer.open({
                type: 2,
                content: '/static/view/dictionary/editDictionary.html?id=' + data.id,
                area: ['45%', '50%'],
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
    active = {
        reload: function () {
            var search_key = $('#search_key');
            var search_value = $('#search_value');
            // 执行重载
            table.reload('dictionaryList', {
                page: {
                    curr: 1
                },
                where: {
                    search_value: search_value.val(),
                    search_key: search_key.val()
                }
            });
        }
    };
    // 添加
    $('#addbtn').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/static/view/dictionary/addDictionary.html',
            area: ['45%', '45%']
        });
    });


});
