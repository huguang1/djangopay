"""djangopay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from apps.system.views import VerifyCodeView, GetConfigGetLoginToken, GetLoginHandler, GetUserNameHandler, \
    MenuUuserMenuListHandler, TDictionaryViewSet, TLookupGroupViewSet, WhiteBlackListViewSet, SysLogViewSet, \
    SysPermissionViewSet, SysRoleViewSet, SysUserViewSet, LogoutHandler
from apps.pay.views import TPayCodeViewSet, TLookupItemViewSet, TPayApiViewSet, TPayInfoViewSet
from apps.cfg.views import TCustomerUserViewSet, TGroupViewSet
from apps.order.views import TOrderHisViewSet, TOrderViewSet

router = DefaultRouter()
router.register(r'config/dictionary', TDictionaryViewSet)  # 处理字典的视图集
router.register(r'config/lookupgroup', TLookupGroupViewSet)  # 处理lookup管理视图集
router.register(r'config/blackWhite', WhiteBlackListViewSet)  # 处理系统白名单视图集
router.register(r'config/sys/log', SysLogViewSet)  # 日志管理视图集
router.register(r'config/sys/permission', SysPermissionViewSet)  # 菜单管理视图集
router.register(r'config/sys/role', SysRoleViewSet)  # 角色管理视图集
router.register(r'config/sys/user', SysUserViewSet)  # 用户管理视图集
router.register(r'config/payCode', TPayCodeViewSet)  # 支付二维码视图集
router.register(r'config/lookupitem', TLookupItemViewSet)  # 支付类型视图集
router.register(r'config/payapi', TPayApiViewSet)  # 支付平台视图集
router.register(r'config/payinfo', TPayInfoViewSet)  # 支付通道视图集
router.register(r'config/customer', TCustomerUserViewSet)  # 会员列表视图集
router.register(r'config/group', TGroupViewSet)  # 会员分级视图集
router.register(r'config/orderhis', TOrderHisViewSet)  # 历史订单列表视图集
router.register(r'config/order', TOrderViewSet)  # 待处理订单表视图集

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'config/cache', VerifyCodeView.as_view()),  # 登陆校验返回token值
    path(r'config/getlogin/token', GetConfigGetLoginToken.as_view()),  # 验证码
    path(r'check/login', GetLoginHandler.as_view()),  # 登陆校验返回token值
    path(r'config/init/getUserName', GetUserNameHandler.as_view()),  # 获取登陆管理员
    path(r'config/menu/userMenuList', MenuUuserMenuListHandler.as_view()),  # 获取到首页菜单
    path(r'logout', LogoutHandler.as_view()),  # 退出
]
