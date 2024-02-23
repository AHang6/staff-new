"""
URL configuration for test_staff_new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from app01 import views
from app01.views import depart, user, mobile, admin, login

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/<int:nid>/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:nid>/delete/', user.user_delete),
    path('user/<int:nid>/edit/', user.user_edit),

    # 靓号管理
    path('mobile/list/', mobile.mobile_list),
    path('mobile/add/', mobile.mobile_add),
    path('mobile/<int:nid>/delete/', mobile.mobile_delete),
    path('mobile/<int:nid>/edit/', mobile.mobile_edit),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 用户登录
    path('login/', login.login),
    path('logout/', login.logout),
    path('image/code/', login.image_code),


]
