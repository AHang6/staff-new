from django import forms
from django.shortcuts import render, redirect

from app01.models import UserInfo
from app01.utils.pagination import Pagination


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
