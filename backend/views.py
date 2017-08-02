from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import simplejson
from .models import Post,Room,User


# Create your views here.

@csrf_exempt
def get_test(request):
    response = JsonResponse(
        {'msg': 'GET Request!'})
    return response

@csrf_exempt
def make_room(request):
    req = simplejson.load(request)
    roomname = req['roomname']
    authId=req['authId']
    myuser=User.objects.get(id=1)
    Room.objects.create(author=myuser,roomName= roomname)
    response = JsonResponse(
        {'msg': 'Making a room successfully!'})
    return response

@csrf_exempt
def list_room(request):
    rooms=Room.objects.order_by('-createTime')
    response = JsonResponse(
        {'rooms': rooms})
    return response

@csrf_exempt
def post_test(request):
    req = simplejson.load(request)
    response = JsonResponse({
        'account': req['account'],
        'password': req['password']
    })
    return response
# Create your views here.
