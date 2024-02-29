import os
from django.shortcuts import render, redirect
from django import forms

from app01.models import City
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm


class CityForm(BootstrapForm):
    bootstrap_exclude = ['img']

    # img = forms.CharField(
    #     label='logo',
    #     widget=forms.FileField,
    # )
    #
    # name = forms.CharField(
    #     label='城市名称',
    #     widget=forms.TextInput,
    # )
    #
    # count = forms.CharField(
    #     label='人数',
    #     widget=forms.TextInput,
    # )

    name = forms.CharField(label='城市名称')
    count = forms.IntegerField(label='人数')
    img = forms.FileField(label='logo')


class CityModelForm(BootstrapModelForm):
    bootstrap_exclude = ['img']

    class Meta:
        model = City
        fields = '__all__'


def City_list(request):
    city_data = City.objects.all()
    page_obj = Pagination(request, city_data)
    context = {
        'city_data': page_obj.page_queryset,
        'page_string': page_obj.html()
    }

    return render(request, 'city_list.html', context)


def city_add(request):
    if request.method == "GET":
        form = CityForm()
        return render(request, 'city_add.html', {'form': form})

    form = CityForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        img_obj = request.FILES.get('img')
        db_path = os.path.join('static', 'img', img_obj.name)

        file_path = os.path.join('app01', db_path)

        f = open(file_path, mode='wb')
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()

        data_dict = {
            'name': form.cleaned_data.get('name'),
            'count': form.cleaned_data.get('count'),
            'img': db_path,
        }

        City.objects.create(**data_dict)
        return redirect('/city/list/')

    return render(request, 'city_add.html', {'form': form})


def city_model_add(request):
    if request.method == 'GET':
        form = CityModelForm()
        return render(request, 'city_add.html', {'form': form})

    form = CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')

    return render(request, 'city_add.html', {'form': form})