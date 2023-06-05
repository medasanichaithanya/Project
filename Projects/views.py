from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Projects.models import *
import base64
from django.core.cache import cache
from .decarator import auth_check, check_rate_limit

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
    
@csrf_exempt
def studentdetails(request):
    if request.method == 'GET':
        try:
            studentdata = studentdetails.objects.filter()
            return JsonResponse({'Status':'NA','Data':studentdata})
        
        except Exception as e:
            return JsonResponse({'Status': 'Error occured'})


    else:
        return JsonResponse({'Status': 'UNKNOWN ERROR'})
    
@csrf_exempt
def inboundapi(request):
    if request.method == 'POST':
        to_params=False
        from_params=False
        try:
            authication = auth_check(request)
            if not authication:
                return JsonResponse({"message": "authentication is failing"},status=403)
           
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            to_param = body['to'] if body['to']  else  ''
            if 6<=len(to_param)<=16 :
                check_to_param = Phone_number.objects.filter(number=int(to_param))
                if check_to_param:
                    to_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            from_param = body['from']  if  body['from'] else  ''
            if 6<=len(from_param)<=16:
                check_to_param = Phone_number.objects.filter(number=from_param)
                if from_param:
                    from_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            text = body['text']  if  body['text'] else  ''
            if 1<=len(text)<=120 and from_params and to_params:
                  if "STOP".strip() in text:
                    cache.set('to',to_param,timeout=5000)
                    cache.set('from',from_param,timeout=5000)
                  return JsonResponse({"message": "inbound sms ok", "error": ""})               
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})
        except Exception as e:
            return JsonResponse({"message": "", "error":"unknown failure"})
    else:
        return JsonResponse({'message':"method not Allowed"},status=405)
    
@csrf_exempt
def outboundapi(request):
    limit_check,from_param = check_rate_limit(request)
    if not limit_check:
        return JsonResponse({'message': "","error":f"limit reached for from {from_param}" })
    if request.method == 'POST':
        to_params=False
        from_params=False
        try:
            authication = auth_check(request)
            if not authication:
                return JsonResponse({"message": "authentication is failing"},status=403)
           
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            to_param = body['to'] if body['to']  else  ''
            if 6<=len(to_param)<=16 :
                check_to_param = Phone_number.objects.filter(number=int(to_param))
                if check_to_param:
                    to_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            from_param = body['from']  if  body['from'] else  ''
            if 6<=len(from_param)<=16:
                check_to_param = Phone_number.objects.filter(number=from_param)
                if from_param:
                    from_params = True
                else:
                    return JsonResponse({"message": "", "error": "to param is not found"})
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})

            text = body['text']  if  body['text'] else  ''
            if 1<=len(text)<=120 and from_params and to_params:
                  check_to_cache = cache.get('to')
                  check_from_cache = cache.get('from')
                  if check_to_cache and check_from_cache:
                      return JsonResponse({"message": "", "error": f"""sms from {from_param} to {to_param} blocked by STOP request"""})  
                  else:
                    return JsonResponse({"message": "outbound sms ok", "error": ""})            
            else:
                return JsonResponse({"message": "", "error": "to param is invalid"})
        except Exception as e:
            return JsonResponse({'message': '', 'error':'unknown failure'})
    else:
        return JsonResponse({'message':'method not Allowed', 'status_code': '405'})