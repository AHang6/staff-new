from django import forms
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from app01.utils.encrypt import md5
from app01.models import Admin
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm


def admin_list(request):
    admin_data = Admin.objects.all()

    page_obj = Pagination(request, admin_data)

    context = {
        'admin_data': page_obj.page_queryset,
        'page_string': page_obj.html()
    }

    return render(request, 'admin_list.html', context)


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)  # 不清空
    )

    class Meta:
        model = Admin
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = Admin.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名存在请重新输入')
        return username

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError('密码输入不一致，请重新输入')

        return confirm_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def admin_add(request):
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'admin_add.html', {'form': form})

    form = AdminModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'admin_add.html', {'form': form})


def admin_delete(request, nid):
    Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = Admin.objects.exclude(id=self.instance.pk).filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username


def admin_edit(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_obj)
        return render(request, 'admin_edit.html', {'form': form})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_edit.html', {'form': form})


class AdminResetModelForm(BootstrapModelForm):
    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)  # 不清空
    )

    class Meta:
        model = Admin
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = md5(self.cleaned_data.get('password'))
        exists = Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        if exists:
            raise ValidationError('新密码不可与原密码相同')
        return pwd

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_pwd'))
        print(pwd, confirm_pwd)
        if pwd:
            if pwd != confirm_pwd:
                raise ValidationError('密码输入不一致')
        return confirm_pwd


def admin_reset(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'admin_reset.html', {'form': form})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        print(form.cleaned_data.get('password'))
        print(form.cleaned_data['password'])
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_reset.html', {'form': form})
