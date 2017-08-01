from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import User
import simplejson
import random
# Create your views here.


@csrf_exempt
def get_test(request):
    response = JsonResponse(
        {'msg': 'GET Request!'})
    return response


@csrf_exempt
def getVerification(request):
    req = simplejson.load(request)
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    verification = []
    for i in range(6):
        verification.append(random.choice(seed))
    salt = ''.join(verification)
    send_mail('Ur verification code!', salt,
              'a1137901181@163.com', [req['account']], fail_silently=False)
    response = JsonResponse({
        'verification': salt,
    })
    return response


@csrf_exempt
def signUp(request):
    req = simplejson.load(request)
    user = User.objects.create_user(
        username=req['account'], password=req['password'], email=req['account'])
    user.save()
    response = JsonResponse({})
    return response
# Create your views here.
