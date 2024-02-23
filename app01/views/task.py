import json
import datetime
import random

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse

from app01.models import Task
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = Task
        fields = "__all__"


@csrf_exempt
def task_list(request):
    if request.method == "GET":
        task_data = Task.objects.all()
        page_obj = Pagination(request, task_data)

        form = TaskModelForm()

        context = {
            'task_data': page_obj.page_queryset,
            'page_string': page_obj.html(),
            'form': form,
        }
        return render(request, 'task_list.html', context)

    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_test(request):
    # print(request.GET)
    print(request.POST)
    data_dict = {'status': True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


def task_delete(request):
    nid = request.GET.get('nid')
    Task.objects.filter(id=nid).delete()
    data_dict = {'status': True}
    return HttpResponse(json.dumps(data_dict))
