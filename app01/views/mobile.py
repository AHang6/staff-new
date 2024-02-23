from django import forms
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01.models import MobileNum
from app01.utils.pagination import Pagination


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
