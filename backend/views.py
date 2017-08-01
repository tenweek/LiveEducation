from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import simplejson
from .models import Post


# Create your views here.

@csrf_exempt
def get_test(request):
    response = JsonResponse(
        {'msg': 'GET Request!'})
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
