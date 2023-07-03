layui.use(['table', 'layer',], function () {
    var $ = layui.jquery, layer = layui.layer;
    var table = layui.table;
    var headData = getHead();
    var tableIns = table.render({
        elem: '#groupList',
        url: window.parent.baseUrl + '/group',
        method: 'get',
        cols: [headData],
        page: true //是否显示分页
        , parseData: function (res) {
            return {
                "code": 0,
                'msg': '',
                "count": res.count,
                "data": res.results
            }
        }
        , limit: 10,
        limits: [5, 10, 100]
        //添加权限控制
        ,
        done: function () {}
    });

    //监听工具条
    table.on('tool(demo)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.confirm('真的删除行么', function (index) {
                $.ajax({
                    type: "delete",
                    url: "/config/group/" + data.id + "/",
                    data: {},
                    dataType: "json",
                    success: function (data, textStatus, xhr) {
                        if (xhr.status == 204){
                            layer.msg("删除成功");
                        }else {
                            layer.msg("删除失败");
                        }
                        setTimeout(function () {
                            active.reload();
                        }, 1000);
                    }
                });
                layer.close(index);
            });
        } else if (obj.event === 'edit') {
            var groupId = data.groupId;
            layer.open({
                type: 2,
                content: '/static/view/customer/editGroupInfo.html?id=' + data.id,
                area: ['30%', '80%']
            });
        }
    });
    active = {
        reload: function () {
            // 执行重载
            table.reload('groupList', {
                page: {
                    curr: 1
                }
            });
        }
    };
    // 添加
    $('#add').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/static/view/customer/addGroupInfo.html',
            area: ['30%', '30%']
        });
    });


});
//获取表头
function getHead() {
    var data = null;
    //数据库里面检查
    $.ajax({
        type: "get",  //使用提交的方法 post、get
        url: "/config/lookupitem/?group_code=PAY_TYPE&state=1",   //提交的地址
        async: false,   //配置是否异步操作
        dataType: "json",//返回数据类型的格式
        data: {"all": "all"}
    }).done(function (result) {//回调操作
        data = result;
    });
    var head = [];
    //ID 表头
    var headitemtype = {};
    headitemtype.field = 'id';
    headitemtype.title = 'ID';
    headitemtype.sort = true;
    headitemtype.align = 'center';
    head.push(headitemtype);

    //分级名称表头
    var headlevel = {};
    headlevel.field = 'name';
    headlevel.title = '分级名称';
    headlevel.align = 'center';
    head.push(headlevel);
    //动态表头
    for (var i in data) {
        if (!isNaN(i)) {
            var headitem = {};
            headitem.field = data[i].item_code;
            headitem.title = data[i].item_name;
            headitem.align = 'center';
            head.push(headitem);
        }
    }
    //工具栏表头
    var headtool = {};
    headtool.title = '操作';
    headtool.align = 'center';
    headtool.fixed = 'right';
    headtool.toolbar = '#barDemo';
    head.push(headtool);
    return head;
}