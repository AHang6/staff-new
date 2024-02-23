import json
import random
from datetime import datetime
from django.http import JsonResponse

from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Older
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm


class OlderAddModelForm(BootstrapModelForm):
    class Meta:
        model = Older
        exclude = ['older', 'user']


@csrf_exempt
def older_list(request):
    older_data = Older.objects.all()
    page_obj = Pagination(request, older_data)

    form = OlderAddModelForm()

    context = {
        'older_data': page_obj.page_queryset,
        'page_string': page_obj.html(),
        'form': form,
    }

    return render(request, 'older_list.html', context)


@csrf_exempt
def older_add(request):
    form = OlderAddModelForm(data=request.POST)
    if form.is_valid():
        # 自动生成订单号
        form.instance.older = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

        # 自动填写用户
        form.instance.user_id = request.session['info']['id']
        print(request.session)

        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {
        'status': False,
        'errors': form.errors,
    }
    return HttpResponse(json.dumps(data_dict))


def older_delete(request):
    nid = request.GET.get('nid')
    Older.objects.filter(id=nid).delete()
    data_dict = {'status': True}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def older_edit(request):
    nid = request.GET.get('nid')
    row_obj = Older.objects.filter(id=nid).values('title', 'price', 'status').first()
    if row_obj:
        data_dict = {'status': True, 'data': row_obj}
        return JsonResponse(data_dict)

    data_dict = {'status': True, 'data': '信息有误，请重新输入'}
    return JsonResponse(data_dict)


@csrf_exempt
def older_edit_save(request):
    nid = request.GET.get('nid')

    row_obj = Older.objects.filter(id=nid).first()
    form = OlderAddModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return JsonResponse(data_dict)

    data_dict = {'status': False, 'errors': form.errors}
    return JsonResponse(data_dict)
