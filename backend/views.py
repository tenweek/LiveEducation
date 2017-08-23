from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate
import simplejson
from .models import Room, User, RoomStudent, VideoRoom
import os
import random
import cloudconvert
import zipfile
import types
import shutil
# Create your views here.


@csrf_exempt
def getVideoRoomInfo(request):
    req = simplejson.load(request)
    videoRoom = VideoRoom.objects.get(id=req['roomId'])
    response = JsonResponse({
        'liveRoomId': videoRoom.live_room_id
    })
    return response


@csrf_exempt
def getVideoRooms(request):
    req = simplejson.load(request)
    if req['type'] == 1:
        rooms = VideoRoom.objects.order_by('-create_time')[:12]
    else:
        rooms = VideoRoom.objects.order_by('-create_time')
    myroom = []
    for room in rooms:
        userImg = room.video_img
        myroom.append({
            'roomName': room.room_name,
            'teacherName': room.teacher.name,
            'liveId': room.live_room_id,
            'userImg': userImg
        })
    response = JsonResponse({'rooms': myroom})
    return response


@csrf_exempt
def startRecord(request):
    req = simplejson.load(request)
    channel = req['channel']
    connect = './backend/record/Recorder_local \
        --appId "9b343e8aaaa144928e093b29513634e9" \
        --uid 0 \
        --channel "' + channel + '" \
        --appliteDir "./backend/record/bin/" \
        --channelProfile 1 \
        --idle 10 \
        --recordFileRootDir "./frontend/static/record/"'
    os.system(connect)
    path = './frontend/static/record/' + \
        req['time'] + '/' + str(req['channel']) + '*'
    command = 'python ./backend/video_convert.py ' + path
    os.system(command)
    os.system('mv ' + path + '/*.mp4 ' +
              './frontend/static/record/' + str(req['channel']) + '.mp4')
    response = JsonResponse({})
    return response


@csrf_exempt
def closeLiveRoom(request):
    req = simplejson.load(request)
    teacherRoom = Room.objects.get(id=req['roomId'])
    RoomStudent.objects.filter(room=teacherRoom).delete()
    VideoRoom.objects.create(teacher=teacherRoom.teacher, room_name=teacherRoom.room_name, live_room_id=teacherRoom.id, video_img=str(
        teacherRoom.teacher.user_img)[22:], file_num=teacherRoom.teacher.file_num)
    oldDir = "./frontend/static/ppt/" + str(teacherRoom.teacher.id) + "and"
    if teacherRoom.teacher.file_num != 0:
        for fileNum in range(1, teacherRoom.teacher.file_num + 1):
            os.rename(oldDir + str(fileNum), oldDir +
                      str(fileNum) + "and" + str(teacherRoom.id))
    teacherRoom.teacher.user_img = ''
    teacherRoom.teacher.user_file = ''
    teacherRoom.teacher.file_num = 0
    teacherRoom.teacher.save()
    Room.objects.filter(id=req['roomId']).delete()
    response = JsonResponse({})
    return response


@csrf_exempt
def killVideoRoom(roomId):
    videoRoom = VideoRoom.objects.get(live_room_id=roomId)
    os.remove("./frontend/static/cover/" + videoRoom.video_img)
    if videoRoom.file_num != 0:
        for file in range(1, videoRoom.file_num + 1):
            shutil.rmtree("./frontend/static/ppt/" + str(videoRoom.teacher.id) +
                          "and" + str(file) + "and" + str(videoRoom.live_room_id))
    VideoRoom.objects.filter(live_room_id=roomId).delete()
    return


@csrf_exempt
def fileFormat(file):
    oldFormat = "ppt"
    if file.name[-1] == 'x':
        oldFormat = "pptx"
    elif file.name[-1] == 'y':
        oldFormat = "key"
    elif file.name[-1] == 'f':
        oldFormat = "pdf"
    else:
        oldFormat = "ppt"
    return oldFormat


@csrf_exempt
def convertFile(user, file):
    fileDir = './' + str(user.user_file)
    oldFormat = fileFormat(file)
    api = cloudconvert.Api(
        '7AoDsm4GZV8LpmYqZHESw4GKqDo1DcZ3ooQtqWR1fhaKZ-Jiva2gC94GVrYRuEEdfkqWVNBHZFGCIYSZAAh3cA')
    process = api.convert({
        "inputformat": oldFormat,
        "outputformat": "png",
        "input": "upload",
        "filename": "user." + oldFormat,
        "file": open(fileDir, 'rb')})
    process.wait()
    process.download('./frontend/static/pptzip/' +
                     str(user.id) + 'and' + str(user.file_num) + '.zip')
    os.remove(fileDir)
    return


@csrf_exempt
def getTeacherFileInfo(request):
    req = simplejson.load(request)
    user = User.objects.get(name=req['name'])
    pageNum = sum([len(x) for _, _, x in os.walk(
        './frontend/static/ppt/' + str(user.id) + 'and' + str(user.file_num))])
    response = JsonResponse({
        'teacherId': user.id,
        'fileNum': user.file_num,
        'maxPage': pageNum
    })
    return response


@csrf_exempt
def getImg(request):
    req = simplejson.load(request)
    user = User.objects.get(username=req['account'])
    response = JsonResponse({'route': str(user.user_img)[8:]})
    return response


@csrf_exempt
def uploadFile(request):
    file = request.FILES.get('file')
    account = request.session.get('account')
    user = User.objects.get(username=account)
    user.user_file = file
    user.file_num += 1
    user.save()
    convertFile(user, file)
    zip_file = zipfile.ZipFile(
        './frontend/static/pptzip/' + str(user.id) + 'and' + str(user.file_num) + '.zip')
    if os.path.isdir('./frontend/static/ppt/' + str(user.id) + 'and' + str(user.file_num)):
        pass
    else:
        os.mkdir('./frontend/static/ppt/' +
                 str(user.id) + 'and' + str(user.file_num))
    for names in zip_file.namelist():
        zip_file.extract(names, './frontend/static/ppt/' +
                         str(user.id) + 'and' + str(user.file_num))
    zip_file.close()
    response = JsonResponse({})
    return response


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
    uploadFile = request.FILES.get('myfile')
    account = request.session.get('account')
    uploadUser = User.objects.get(username=account)
    oldImg = uploadUser.user_img
    uploadUser.user_img = uploadFile
    uploadUser.save()
    if oldImg != '':
        os.remove('./' + str(oldImg))
    response = JsonResponse({})
    return response


@csrf_exempt
def kickOut(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(username=request.session.get('account'))
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
    student = User.objects.get(username=request.session.get('account'))
    roomStudent = RoomStudent.objects.get(room=room, student=student)
    response = JsonResponse({'result': roomStudent.can_speak})
    return response


@csrf_exempt
def gag(request):
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(username=request.session.get('account'))
    roomStudent = RoomStudent.objects.get(room=room, student=student)
    roomStudent.can_speak = False
    roomStudent.save()
    response = JsonResponse({})
    return response


@csrf_exempt
def getRoomInfo(request):
    if not request.session.get('account'):
        response = JsonResponse({
            'result': False
        })
        return response
    req = simplejson.load(request)
    room = Room.objects.filter(id=req['roomID'])
    if len(room) == 0:
        response = JsonResponse({
            'result': False
        })
        return response
    student = User.objects.get(username=request.session.get('account'))
    roomStudent = RoomStudent.objects.filter(room=room, student=student)
    if len(roomStudent) == 0:
        RoomStudent.objects.create(room=room[0], student=student)
    elif not roomStudent[0].can_watch:
        response = JsonResponse({
            'result': False
        })
        return response
    response = JsonResponse({
        'result': True,
        'teacherName': room[0].teacher.name,
        'stuNum': room[0].student_num,
        'roomName': room[0].room_name,
        'name': student.name
    })
    return response


@csrf_exempt
def joinRoom(request):
    if not request.session.get('account'):
        response = JsonResponse({
            'result': 'login'
        })
        return response
    stuAccount = request.session.get('account')
    req = simplejson.load(request)
    room = Room.objects.get(id=req['roomID'])
    student = User.objects.get(username=stuAccount)
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
    if not request.session.get('account'):
        response = JsonResponse({
            'result': False
        })
        return response
    req = simplejson.load(request)
    user = User.objects.get(username=request.session.get('account'))
    response = JsonResponse({
        'result': True,
        'account': user.username,
        'name': user.name,
        'isTeacher': user.is_teacher
    })
    return response


@csrf_exempt
def createRoom(request):
    req = simplejson.load(request)
    teacher = User.objects.get(username=req['account'])
    room = Room.objects.create(teacher=teacher, room_name=req['roomName'])
    RoomStudent.objects.create(room=room, student=teacher)
    path = "./frontend/static/" + str(room.id)
    os.makedirs(path)
    os.mknod(path + "/" + str(room.id) + ".txt")
    response = JsonResponse({'roomId': room.id})
    return response


@csrf_exempt
def getRooms(request):
    req = simplejson.load(request)
    if req['type'] == 1:
        rooms = Room.objects.order_by('-student_num')[:12]
    else:
        rooms = Room.objects.order_by('-student_num')
    myroom = []
    for room in rooms:
        userImg = str(room.teacher.user_img)
        myroom.append({'roomName': room.room_name,
                       'teacherName': room.teacher.name,
                       'id': room.id,
                       'studentNum': room.student_num,
                       'userImg': userImg[8:]})
    response = JsonResponse(
        {'rooms': myroom})
    return response


@csrf_exempt
def getMailVerification(request):
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
        request.session['account'] = req['account']
        response = JsonResponse({'result': True})
    return response


@csrf_exempt
def logout(request):
    del request.session['account']
    response = JsonResponse({})
    return response


@csrf_exempt
def getMailRand(request):
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
