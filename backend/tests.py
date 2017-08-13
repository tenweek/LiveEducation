# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.http import JsonResponse
from django.contrib.auth import authenticate
from backend.models import Room, User, RoomStudent
import json


#共29个测试
#测试获取房间 2个测试
class TestGetRooms(TestCase):
    def setUp(self):
        User.objects.create(
            name='wenbin', username='1352075893@qq.com', is_teacher=1)
        self.user = User.objects.get(name='wenbin')
        Room.objects.create(teacher=self.user, room_name='room1')
        Room.objects.create(teacher=self.user, room_name='room2')
        Room.objects.create(teacher=self.user, room_name='room3')
        Room.objects.create(teacher=self.user, room_name='room4')
        Room.objects.create(teacher=self.user, room_name='room5')
        Room.objects.create(teacher=self.user, room_name='room6')
        Room.objects.create(teacher=self.user, room_name='room7')
        Room.objects.create(teacher=self.user, room_name='room8')
        Room.objects.create(teacher=self.user, room_name='room9')
        Room.objects.create(teacher=self.user, room_name='room10')
        Room.objects.create(teacher=self.user, room_name='room11')
        Room.objects.create(teacher=self.user, room_name='room12')
        self.c = Client()

    def testGetRoomsType1(self):
        request = json.dumps({'type': 1})
        response = self.c.post('/getRooms/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(req['rooms']), 8)

    def testGetRoomsType2(self):
        request = json.dumps({'type': 2})
        response = self.c.post('/getRooms/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(req['rooms']), 12)

    def tearDown(self):
        Room.objects.filter().delete()
        User.objects.filter().delete()


#测试禁言等 11个测试
class TestSpeakWatch(TestCase):
    def setUp(self):
        User.objects.create(
            name='wenbin1', username='1352075893@qq.com', is_teacher=1)
        User.objects.create(
            name='wenbin2', username='1352075896@qq.com', is_teacher=1)
        User.objects.create(
            name='wenbin3', username='1352075899@qq.com', is_teacher=1)
        self.user1 = User.objects.get(name='wenbin1')
        self.user2 = User.objects.get(name='wenbin2')
        self.user3 = User.objects.get(name='wenbin3')
        Room.objects.create(teacher=self.user1, room_name='room1')
        Room.objects.create(teacher=self.user2, room_name='room2')
        Room.objects.create(teacher=self.user3, room_name='room3')
        self.myroom1 = Room.objects.get(teacher=self.user1)
        self.myroom2 = Room.objects.get(teacher=self.user2)
        self.myroom3 = Room.objects.get(teacher=self.user3)
        RoomStudent.objects.create(room=self.myroom1, student=self.user2)
        RoomStudent.objects.create(room=self.myroom1, student=self.user3)
        RoomStudent.objects.create(room=self.myroom2, student=self.user3)
        RoomStudent.objects.create(room=self.myroom3, student=self.user1)
        self.roomStudent1 = RoomStudent.objects.get(
            room=self.myroom1, student=self.user2)
        self.roomStudent2 = RoomStudent.objects.get(
            room=self.myroom2, student=self.user3)
        self.roomStudent3 = RoomStudent.objects.get(
            room=self.myroom3, student=self.user1)
        self.roomStudent4 = RoomStudent.objects.get(
            room=self.myroom1, student=self.user3)
        self.c = Client()

    def testKickOut1(self):
        request = json.dumps({'roomID': self.myroom1.id, 'name': 'wenbin2'})
        response = self.c.post('/kickOut/', request,
                               content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_watch, False)

    def testKickOut2(self):
        request = json.dumps({'roomID': self.myroom2.id, 'name': 'wenbin3'})
        response = self.c.post('/kickOut/', request,
                               content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom2, student=self.user3).can_watch, False)

    def testKickOut3(self):
        request = json.dumps({'roomID': self.myroom3.id, 'name': 'wenbin1'})
        response = self.c.post('/kickOut/', request,
                               content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom3, student=self.user1).can_watch, False)

    def testGag1(self):
        request = json.dumps({'roomID': self.myroom1.id, 'name': 'wenbin2'})
        response = self.c.post(
            '/gag/', request, content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, False)

    def testGag2(self):
        request = json.dumps({'roomID': self.myroom2.id, 'name': 'wenbin3'})
        response = self.c.post(
            '/gag/', request, content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom2, student=self.user3).can_speak, False)

    def testGag3(self):
        request = json.dumps({'roomID': self.myroom3.id, 'name': 'wenbin1'})
        response = self.c.post(
            '/gag/', request, content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom3, student=self.user1).can_speak, False)

    def testAllowSpeak(self):
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, True)
        self.roomStudent4.can_speak = False
        self.roomStudent4.save()
        self.roomStudent1.can_speak = False
        self.roomStudent1.save()
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, False)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, False)
        request = json.dumps(
            {'roomID': self.myroom1.id, 'student': ['wenbin2', 'wenbin3']})
        response = self.c.post('/allowSpeak/', request,
                               content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, True)

    def testAllowAllSpeak(self):
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, True)
        self.roomStudent4.can_speak = False
        self.roomStudent4.save()
        self.roomStudent1.can_speak = False
        self.roomStudent1.save()
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, False)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, False)
        request = json.dumps({'roomID': self.myroom1.id})
        response = self.c.post('/allowAllSpeak/', request,
                               content_type='application/json')
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, True)

    def testGagAll(self):
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, True)
        request = json.dumps({'roomID': self.myroom1.id})
        response = self.c.post('/gagAll/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(req['gagList']), 2)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, False)
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user3).can_speak, False)

    def testCheckGagTrue(self):
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        request = json.dumps({'roomID': self.myroom1.id, 'name': 'wenbin2'})
        response = self.c.post('/checkGag/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], True)

    def testCheckGagFalse(self):
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, True)
        self.roomStudent1.can_speak = False
        self.roomStudent1.save()
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_speak, False)
        request = json.dumps({'roomID': self.myroom1.id, 'name': 'wenbin2'})
        response = self.c.post('/checkGag/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], False)

    def tearDown(self):
        RoomStudent.objects.filter().delete()
        Room.objects.filter().delete()
        User.objects.filter().delete()


#测试房间管理 6个测试
class TestAboutRoom(TestCase):
    def setUp(self):
        User.objects.create(
            name='wenbin1', username='1352075893@qq.com', is_teacher=1)
        User.objects.create(
            name='wenbin2', username='1352075896@qq.com', is_teacher=0)
        User.objects.create(
            name='wenbin3', username='1352075899@qq.com', is_teacher=1)
        User.objects.create(
            name='wenbin4', username='1352075894@qq.com', is_teacher=1)
        self.user1 = User.objects.get(name='wenbin1')
        self.user2 = User.objects.get(name='wenbin2')
        self.user3 = User.objects.get(name='wenbin3')
        self.user4 = User.objects.get(name='wenbin4')
        Room.objects.create(teacher=self.user1,
                            room_name='room1', student_num=10)
        Room.objects.create(teacher=self.user2, room_name='room2')
        Room.objects.create(teacher=self.user3, room_name='room3')
        self.myroom1 = Room.objects.get(teacher=self.user1)
        self.myroom2 = Room.objects.get(teacher=self.user2)
        self.myroom3 = Room.objects.get(teacher=self.user3)
        RoomStudent.objects.create(room=self.myroom1, student=self.user2)
        RoomStudent.objects.create(room=self.myroom1, student=self.user3)
        RoomStudent.objects.create(room=self.myroom2, student=self.user3)
        RoomStudent.objects.create(room=self.myroom3, student=self.user1)
        self.roomStudent1 = RoomStudent.objects.get(
            room=self.myroom1, student=self.user2)
        self.roomStudent2 = RoomStudent.objects.get(
            room=self.myroom2, student=self.user3)
        self.roomStudent3 = RoomStudent.objects.get(
            room=self.myroom3, student=self.user1)
        self.roomStudent4 = RoomStudent.objects.get(
            room=self.myroom1, student=self.user3)
        self.c = Client()

    def testGetRoomInfo(self):
        request = json.dumps({'roomID': self.myroom1.id})
        response = self.c.post('/getRoomInfo/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['teacherName'], 'wenbin1')
        self.assertEqual(req['stuNum'], 10)
        self.assertEqual(req['roomName'], 'room1')

    def testJoinRoom1(self):
        request = json.dumps(
            {'roomID': self.myroom2.id, 'stuAccount': '1352075893@qq.com'})
        response = self.c.post('/joinRoom/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], self.myroom2.id)

    def testJoinRoom2(self):
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_watch, True)
        self.roomStudent1.can_watch = False
        self.roomStudent1.save()
        self.assertEqual(RoomStudent.objects.get(
            room=self.myroom1, student=self.user2).can_watch, False)
        request = json.dumps(
            {'roomID': self.myroom1.id, 'stuAccount': '1352075896@qq.com'})
        response = self.c.post('/joinRoom/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], 'cannot')

    def testGetNameTrue(self):
        request = json.dumps({'account': '1352075893@qq.com'})
        response = self.c.post('/getName/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['name'], 'wenbin1')
        self.assertEqual(req['isTeacher'], True)

    def testGetNameFalse(self):
        request = json.dumps({'account': '1352075896@qq.com'})
        response = self.c.post('/getName/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['name'], 'wenbin2')
        self.assertEqual(req['isTeacher'], False)

    def testCreateRoom(self):
        request = json.dumps(
            {'roomName': 'room4', 'account': '1352075894@qq.com'})
        response = self.c.post('/createRoom/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['msg'], 'Making a room successfully!')
        self.assertEqual(Room.objects.get(
            teacher=self.user4).room_name, 'room4')

    def tearDown(self):
        RoomStudent.objects.filter().delete()
        Room.objects.filter().delete()
        User.objects.filter().delete()


#测试用户管理 10个测试
class TestAboutUser(TestCase):
    def setUp(self):
        User.objects.create_user(
            name='wenbin1', username='1352075893@qq.com', is_teacher=1, password='smile1314')
        User.objects.create(
            name='wenbin2', username='1352075896@qq.com', is_teacher=1)
        User.objects.create(
            name='wenbin3', username='1352075899@qq.com', is_teacher=1)
        self.user1 = User.objects.get(name='wenbin1')
        self.user2 = User.objects.get(name='wenbin2')
        self.user3 = User.objects.get(name='wenbin3')
        Room.objects.create(teacher=self.user1, room_name='room1')
        Room.objects.create(teacher=self.user2, room_name='room2')
        Room.objects.create(teacher=self.user3, room_name='room3')
        self.myroom1 = Room.objects.get(teacher=self.user1)
        self.myroom2 = Room.objects.get(teacher=self.user2)
        self.myroom3 = Room.objects.get(teacher=self.user3)
        RoomStudent.objects.create(room=self.myroom1, student=self.user2)
        RoomStudent.objects.create(room=self.myroom1, student=self.user3)
        RoomStudent.objects.create(room=self.myroom2, student=self.user3)
        RoomStudent.objects.create(room=self.myroom3, student=self.user1)
        self.c = Client()

    def testGetVerificationExist(self):
        request = json.dumps({'mail': '1352075893@qq.com'})
        response = self.c.post('/getVerification/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['verification'], 'exist')

    def testGetVerificationSalt(self):
        request = json.dumps({'mail': '907836805@qq.com'})
        response = self.c.post('/getVerification/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(req['verification']), 6)

    def testChangeName(self):
        self.assertEqual(self.user1.name, 'wenbin1')
        request = json.dumps(
            {'account': '1352075893@qq.com', 'newname': 'zhizhi'})
        response = self.c.post('/changeName/', request,
                               content_type='application/json')
        self.assertEqual(User.objects.get(
            username='1352075893@qq.com').name, 'zhizhi')

    def testSignUpFalse(self):
        request = json.dumps(
            {'username': 'wenbin1', 'mail': '1352075893@qq.com', 'password': 'smile1314'})
        response = self.c.post('/signUp/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], False)

    def testSignUpTrue(self):
        request = json.dumps(
            {'username': 'wenbin4', 'mail': '1352075894@qq.com', 'password': 'smile1314'})
        response = self.c.post('/signUp/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], True)
        self.assertEqual(User.objects.get(
            name='wenbin4').username, '1352075894@qq.com')

    def testLoginTrue(self):
        request = json.dumps(
            {'account': '1352075893@qq.com', 'password': 'smile1314'})
        response = self.c.post(
            '/login/', request, content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], True)
        self.assertEqual(req['name'], 'wenbin1')

    def testLoginFalse(self):
        request = json.dumps(
            {'account': '1352075893@qq.com', 'password': 'smile1315'})
        response = self.c.post(
            '/login/', request, content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], False)

    def testChangePassword(self):
        self.assertEqual(authenticate(
            username='1352075893@qq.com', password='smile1314'), self.user1)
        request = json.dumps(
            {'username': '1352075893@qq.com', 'password': 'smile1315'})
        response = self.c.post('/changePasswd/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['result'], True)
        self.assertEqual(authenticate(
            username='1352075893@qq.com', password='smile1315'), self.user1)

    def testGetRandNone(self):
        request = json.dumps({'mail': '13702198137@qq.com'})
        response = self.c.post('/getRand/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(req['verification'], 'none')

    def testGetRandSalt(self):
        request = json.dumps({'mail': '1352075893@qq.com'})
        response = self.c.post('/getRand/', request,
                               content_type='application/json')
        req = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(req['verification']), 6)

    def tearDown(self):
        RoomStudent.objects.filter().delete()
        Room.objects.filter().delete()
        User.objects.filter().delete()
# Create your tests here.
