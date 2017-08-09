from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate
import simplejson
from .models import Room, User, RoomStudent, StuBlackList

import random
# Create your views here.


@csrf_exempt
def checkMute(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(name='qq')
    roomStudent = RoomStudent.objects.get(room=room, student=student)
    response = JsonResponse({'result': roomStudent.can_speak})
    return response


@csrf_exempt
def mute(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(name=req['name'])
    roomStudent = RoomStudent.objects.get(room=room, student=student)
    roomStudent.can_speak = False
    roomStudent.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def getRoomInfo(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    response = JsonResponse({
        'teacherName': room.teacher.name,
        'stuNum': room.student_num,
        'roomName': room.room_name
    })
    return response


@csrf_exempt
def joinRoom(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(username=req['stuAccount'])
    if len(RoomStudent.objects.filter(room=room, student=student)) == 0:
        if len(StuBlackList.objects.filter(room=room, student=student)) == 0:
            RoomStudent.objects.create(room=room, student=student)
            room.student_num += 1
            room.save()
            response = JsonResponse({'result': room.id})
            return response
        else:
            response = JsonResponse({'result': 'cannot'})
            return response
    else:
        response = JsonResponse({'result': room.id})
        return response


@csrf_exempt
def getName(request):
    req = simplejson.load(request)
    user = User.objects.get(username=req['account'])
    response = JsonResponse({
        'name': user.name,
        'isTeacher': user.is_teacher
    })
    return response


@csrf_exempt
def createRoom(request):
    req = simplejson.load(request)
    roomName = req['roomName']
    authId = req['account']
    teacher = User.objects.get(username=authId)
    Room.objects.create(teacher=teacher, room_name=roomName)
    response = JsonResponse(
        {'msg': 'Making a room successfully!'})
    return response


@csrf_exempt
def getRooms(request):
    rooms = Room.objects.order_by('-create_time')
    myroom = []
    for room in rooms:
        myroom.append({'roomName': room.room_name,
                       'teacherName': room.teacher.name,
                       'id': room.id,
                       'studentNum': room.student_num})
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
    response = JsonResponse({'verification': salt})
    return response


@csrf_exempt
def signUp(request):
    req = simplejson.load(request)
    userFilterWithName = User.objects.filter(name=req['username'])
    if len(userFilterWithName) != 0:
        response = JsonResponse({'result': False})
        return response
    user = User.objects.create_user(
        username=req['mail'], password=req['password'], name=req['username'])
    user.save()
    response = JsonResponse({'result': True})
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


@csrf_exempt
def changeName(request):
    req = simplejson.load(request)
    user = User.objects.get(username=req['account'])
    user.name = req['newname']
    user.save()
    response = JsonResponse({})
    return response
# Create your views here.
