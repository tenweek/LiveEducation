from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from .models import User
import simplejson
from .models import Room,User

import random
# Create your views here.


@csrf_exempt

@csrf_exempt
def make_room(request):
    req = simplejson.load(request)
    roomname = req['roomname']
    authId=req['authId']
    myuser=User.objects.get(name=authId)
    if myuser.isTeacher:
        Room.objects.create(author=myuser,roomName= roomname)
        response = JsonResponse(
            {'msg': 'Making a room successfully!'})
        return response
    else:
        response = JsonResponse(
            {'msg': 'Sorry! You are not a teacher'})
        return response

@csrf_exempt
def list_room(request):
    rooms = Room.objects.order_by('-createTime')
    myroom = []
    for room in rooms:
        myroom.append({'roomname': room.roomName,'username': room.author.name})
    response = JsonResponse(
        {'rooms': myroom})
    return response

@csrf_exempt
def getVerification(request):
    req = simplejson.load(request)
    user = User.objects.filter(username=req['mail'])
    if len(user) != 0:
        response = JsonResponse({'verification': 'exist'})
        return response
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    verification = []
    for i in range(6):
        verification.append(random.choice(seed))
    salt = ''.join(verification)
    send_mail('Ur verification code!', salt,
              'a1137901181@163.com', [req['mail']], fail_silently=False)
    response = JsonResponse({'verification': salt, })
    return response


@csrf_exempt
def signUp(request):
    req = simplejson.load(request)
    user = User.objects.create_user(
        username=req['mail'], password=req['password'], name=req['username'])
    user.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def login(request):
    req = simplejson.load(request)
    user = authenticate(username=req['account'], password=req['password'])
    if user is None:
        response = JsonResponse({'result': False})
    else:
        response = JsonResponse({'result': True, 'name': user.name})
    return response


@csrf_exempt
def getRand(request):
    req = simplejson.load(request)
    user = User.objects.filter(username=req['mail'])
    if len(user) == 0:
        response = JsonResponse({'verification': 'none'})
        return response
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    verification = []
    for i in range(6):
        verification.append(random.choice(seed))
    salt = ''.join(verification)
    send_mail('Ur verification code!', salt,
              'a1137901181@163.com', [req['mail']], fail_silently=False)
    response = JsonResponse({'verification': salt})
    return response

@csrf_exempt
def changePasswd(request):
    req = simplejson.load(request)
    user = User.objects.get(username=req['username'])
    user.set_password(req['password'])
    user.save()
    response = JsonResponse({'result': True})
    return response
# Create your views here.
