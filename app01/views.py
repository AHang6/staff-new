from django import forms
from django.shortcuts import render, redirect

from app01.models import Depart, UserInfo


# Create your views here.

def depart_list(request):
    depart_data = Depart.objects.all()

    return render(request, 'depart_list.html', {'depart_data': depart_data})


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
    return render(request, "user_list.html", {'user_data': user_data})


class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = "__all__"

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
