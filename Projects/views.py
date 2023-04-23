from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Projects.models import *

# Create your views here.
@csrf_exempt
def fetchwaist(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            height = body['height']
            age = body['age']
            weight = body['weight']
            fetch_waist = Information.objects.filter(height=height, age=age, weight=weight).values('waist')
            if fetch_waist:
                return JsonResponse({'Status': 'SUCCESS' ,'Waist':fetch_waist[0]['waist']})
            else:
                return JsonResponse({'Status': 'Failed'})

        except Exception as e:
            return JsonResponse({'Status': 'Error occured'})
    else:
        return JsonResponse({'Status': 'UNKNOWN ERROR'})

@csrf_exempt
def updatewaist(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            height = body['height']
            age = body['age']
            weight = body['weight']
            waist = body['waist']
            update_record = Information(height=height, age=age, weight=weight, waist=waist)
            update_record.save()
            return JsonResponse({'Status': 'SUCCESS'})
        
        except Exception as e:
            return JsonResponse({'Status': 'Error occured'})
    else:
        return JsonResponse({'Status': 'UNKNOWN ERROR'})