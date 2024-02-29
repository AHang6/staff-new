from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    legend_list = {
        'data': ['销量', '价格'],
    }
    x_axis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']

    series = [
        {
            'name': '销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '价格',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        }
    ]

    result = {
        'status': True,
        'data': {
            'legend_list': legend_list,
            'x_axis': x_axis,
            'series': series
        }
    }
    return JsonResponse(result)
