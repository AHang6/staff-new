from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse
from django import forms

from app01.models import Admin
from app01.utils.encrypt import md5
from app01.utils.image_code import check_code
from app01.utils.bootstrap import BootstrapForm


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
