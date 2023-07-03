layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate'], function () {
    var table = layui.table;
    var laydate = layui.laydate;
    //日期时间选择器
    laydate.render({
        elem: '#endTime'
        , type: 'datetime'
    });
    laydate.render({
        elem: '#createTime'
        , type: 'datetime'
    });
    var tableIns = table.render({
        elem: '#log-table-reload',
        url: window.parent.baseUrl + '/sys/log',
        cols: [[
            {checkbox: true, fixed: 'left'},
            {field: 'id', title: 'ID'},
            {field: 'business', title: '日子内容', sort: true},
            {field: 'model', title: '模块'},
            {field: 'log_params', title: '参数'},
            {field: 'log_ip', title: 'IP'},
            {field: 'log_user', title: '操作人'},
            {field: 'create_time', title: '操作时间'}
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
    });
    //监听工具条
    var $ = layui.$, active = {
        getCheckData: function () { //获取选中数据
            var checkStatus = table.checkStatus('log-table-reload'),
                data = checkStatus.data;
        },
        batchDelete: function () { //批量删除
            var checkStatus = table.checkStatus('log-table-reload'),
                data = checkStatus.data;
            if (data.length == 0) {
                layer.alert("没有选中数据！");
                return false;
            } else {
                layer.confirm('确认删除所有日志吗？', function (index) {
                    if (index) {
                        var str = '';
                        for (var i = 0; i < data.length; i++) {
                            if (str == '') {
                                str += data[i].id;
                            } else {
                                str += ',' + data[i].id;
                            }
                        }
                        $.ajax({
                            type: 'delete',
                            url: window.parent.baseUrl + '/sys/log/aa/',
                            data: {logIds: str},
                            dataType: 'json',
                            success: function (result, textStatus, xhr) {
                                if (xhr.status == 204) {
                                    layer.alert('删除日志成功', {
                                        icon: 6,
                                        title: "提示"
                                    });
                                } else {
                                    layer.alert('删除日志失败', {
                                        icon: 5,
                                        title: "提示"
                                    });
                                }
                                //表格重载
                                tableIns.reload({
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                            }
                        });
                    }
                });
            }
        },
        clearDelete: function () { //清空数据
            layer.confirm('确认清空所有日记吗？', function (index) {
                $.ajax({
                    type: 'delete',
                    url: window.parent.baseUrl + '/sys/log/all/',
                    success: function (result, textStatus, xhr) {
                        if (xhr.status == 204) {
                            layer.alert('删除成功', {
                                icon: 6,
                                title: "提示"
                            });
                        } else {
                            layer.alert('删除成功', {
                                icon: 5,
                                title: "提示"
                            });
                        }
                        //表格重载
                        tableIns.reload({
                            page: {
                                curr: 1 //重新从第 1 页开始
                            }
                        });
                    }
                });
            });

        },
        reload: function () {
            var logUser = $('#logUser').val();
            var createTime = $('#createTime').val();
            var endTime = $('#endTime').val();
            //执行重载
            table.reload('log-table-reload', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    logUser: logUser,
                    createTime: createTime,
                    endTime: endTime
                }
            });
        }
    };
    $('.layui-btn ').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});