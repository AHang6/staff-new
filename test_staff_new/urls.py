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
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.views import depart, user, mobile, admin, login, task, older, chart, city

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),


    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/multi/', depart.depart_multi),
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

    # 任务管理
    path('task/list/', task.task_list),
    path('task/test/', task.task_test),
    path('task/delete/', task.task_delete),

    # 订单管理
    path('older/list/', older.older_list),
    path('older/add/', older.older_add),
    path('older/delete/', older.older_delete),
    path('older/edit/', older.older_edit),
    path('older/edit/save/', older.older_edit_save),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),

    # 城市列表
    path('city/list/', city.City_list),
    path('city/add/', city.city_add),
    path('city/model/add/', city.city_model_add),

]
