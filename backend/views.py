from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate
import simplejson
from .models import Room, User, RoomStudent

import random
# Create your views here.


@csrf_exempt
def changeNum(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomId'])
    room.student_num = req['studentNum']
    room.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def upload(request):
    nowFile = request.FILES.get('myfile')
    account = request.COOKIES.get('userAccount')
    nowUser = User.objects.get(username = account)
    nowUser.user_img = nowFile
    nowUser.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def kickOut(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(name=req['name'])
    roomStudent = RoomStudent.objects.get(room=room, student=student)
    roomStudent.can_watch = False
    roomStudent.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def allowAllSpeak(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    roomStudents = RoomStudent.objects.filter(room=room)
    for roomStudent in roomStudents:
        roomStudent.can_speak = True
        roomStudent.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def allowSpeak(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    for name in req['student']:
        student = User.objects.get(name=name)
        roomStudent = RoomStudent.objects.get(room=room, student=student)
        roomStudent.can_speak = True
        roomStudent.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def gagAll(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    roomStudents = RoomStudent.objects.filter(room=room)
    stu = []
    for roomStudent in roomStudents:
        roomStudent.can_speak = False
        stu.append(roomStudent.student.name)
        roomStudent.save()
    response = JsonResponse({'gagList': stu})
    return response


@csrf_exempt
def checkGag(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(name=req['name'])
    roomStudent = RoomStudent.objects.get(room=room, student=student)
    response = JsonResponse({'result': roomStudent.can_speak})
    return response


@csrf_exempt
def gag(request):
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
    roomStudent = RoomStudent.objects.filter(room=room, student=student)
    if len(roomStudent) == 0:
        RoomStudent.objects.create(room=room, student=student)
        response = JsonResponse({'result': room.id})
        return response
    elif roomStudent[0].can_watch == False:
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
    print(request.POST)
    req = simplejson.load(request)
    roomName = req['roomName']
    authId = req['account']
    teacher = User.objects.get(username=authId)
    print(teacher.user_img)
    Room.objects.create(teacher=teacher, room_name=roomName)
    response = JsonResponse({})
    return response


@csrf_exempt
def getRooms(request):
    req = simplejson.load(request)
    if req['type'] == 1:
        rooms = Room.objects.order_by('-create_time')[:8]
    else:
        rooms = Room.objects.order_by('-create_time')
    myroom = []
    for room in rooms:
        userImg = str(room.teacher.user_img)
        print(userImg[8:])
        myroom.append({'roomName': room.room_name,
                       'teacherName': room.teacher.name,
                       'id': room.id,
                       'studentNum': room.student_num,
                       'userImg': userImg[8:]})
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
    userFilterWithName = User.objects.filter(name=req['newname'])
    if len(userFilterWithName) != 0:
        response = JsonResponse({'result': False})
        return response
    user = User.objects.get(username=req['account'])
    user.name = req['newname']
    user.save()
    response = JsonResponse({'result': True})
    return response
# Create your views here.
