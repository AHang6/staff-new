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

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 部门管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/<int:nid>/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    # 用户管理
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/delete/', views.user_delete),
    path('user/<int:nid>/edit/', views.user_edit),

    # 靓号管理
    path('mobile/list/', views.mobile_list),
    path('mobile/add/', views.mobile_add),
    path('mobile/<int:nid>/delete/', views.mobile_delete),
    path('mobile/<int:nid>/edit/', views.mobile_edit),

    # 管理员管理
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/delete/', views.admin_delete),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/reset/', views.admin_reset),

]
