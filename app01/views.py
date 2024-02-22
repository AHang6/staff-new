from io import BytesIO

from django import forms
from django.shortcuts import render, redirect, HttpResponse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapForm
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.image_code import check_code
from app01.models import Depart, UserInfo, MobileNum, Admin


# Create your views here.

def depart_list(request):
    depart_data = Depart.objects.all()

    page_obj = Pagination(request, depart_data)

    context = {
        'depart_data': page_obj.page_queryset,
        'page_string': page_obj.html()
    }

    return render(request, 'depart_list.html', context)


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')

    depart_title = request.POST.get('title')
    exists = Depart.objects.filter(title=depart_title).exists()
    if not exists:
        Depart.objects.create(title=depart_title)
    else:
        return render(request, 'depart_add.html', {'error_msg': '部门名称存在请重新输入'})

    return redirect('/depart/list/')


def depart_delete(request, nid):
    Depart.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit(request, nid):
    if request.method == "GET":
        depart_info = Depart.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'depart_info': depart_info})

    title_new = request.POST.get('title')
    Depart.objects.filter(id=nid).update(title=title_new)
    return redirect('/depart/list/')


def user_list(request):
    user_data = UserInfo.objects.all()

    page_obj = Pagination(request, user_data)
    context = {
        'user_data': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }
    return render(request, "user_list.html", context)


class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def user_add(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "user_add.html", {'form': form})

    form = UserForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, 'user_add.html', {'form', form})


def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def user_edit(request, nid):
    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserForm(instance=row_object)
        return render(request, "user_edit.html", {'form': form})

    form = UserForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_edit.html', {'form': form})


class MobileForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = MobileNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = MobileNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号重复')
        return txt_mobile


def mobile_list(request):
    data_dict = {}
    search_info = request.GET.get('q', "")

    if search_info:
        data_dict['mobile__contains'] = search_info

    queryset = MobileNum.objects.filter(**data_dict).order_by('-level')
    page_obj = Pagination(request, queryset)

    context = {
        'search_info': search_info,
        'mobile_data': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, "mobile_list.html", context)


def mobile_add(request):
    if request.method == "GET":
        form = MobileForm()
        return render(request, "mobile_add.html", {'form': form})

    form = MobileForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/mobile/list/')
    return render(request, "mobile_add.html", {'form': form})


def mobile_delete(request, nid):
    MobileNum.objects.filter(id=nid).delete()
    return redirect('/mobile/list/')


class MobileEditForm(forms.ModelForm):
    class Meta:
        model = MobileNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = MobileNum.objects.filter(mobile=txt_mobile).exclude(id=self.instance.pk).exists()
        if exists:
            raise ValidationError('手机号存在请重新输入')
        return txt_mobile


def mobile_edit(request, nid):
    row_object = MobileNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = MobileEditForm(instance=row_object)
        return render(request, 'mobile_edit.html', {'form': form})

    form = MobileEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/mobile/list/')

    return render(request, 'mobile_edit.html', {'form': form})


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


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput()
    )

    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True)  # 不清空
    )

    image_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)

    if form.is_valid():
        user_code = form.cleaned_data.pop('image_code')
        code_string = request.session.get('image_code')

        # 账号密码校验
        admin_obj = Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error('password', '密码输入错误请重新输入')
            return render(request, 'login.html', {'form': form})

        # 验证码内容校验
        if user_code.upper() != code_string.upper():
            print(code_string, user_code)
            form.add_error('image_code', '验证码输入错误')
            return render(request, 'login.html', {'form': form})

        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        request.session.set_expiry(60 * 60 * 24 * 7)  # session有效期7天
        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    # 清楚session 信息
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    img, code_string = check_code()
    print(code_string)

    request.session['image_code'] = code_string
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


