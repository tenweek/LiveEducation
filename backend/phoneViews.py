# -*- coding: utf-8 -*
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
import simplejson
import random
import base64
import datetime
import urllib2
import md5


##返回签名
def getSig(accountSid, accountToken, timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()


##发送HTTP请求
def urlOpen(req, data=None):
    try:
        res = urllib2.urlopen(req, data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data


##生成HTTP报文
def createHttpReq(req, url, accountSid, timestamp, responseMode, body):
    req.add_header("Authorization", getAuth(accountSid, timestamp))
    if responseMode:
        req.add_header("Accept", "application/" + responseMode)
        req.add_header("Content-Type", "application/" +
                       responseMode + ";charset=utf-8")
    if body:
        req.add_header("Content-Length", len(body))
        req.add_data(body)
    return req


##生成授权信息
def getAuth(accountSid, timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()


##发送短信验证码
#@param accountSid 主帐号ID
#@param accountToken 主帐号Token
#@param appId 应用ID
#@param toNumbers 被叫的号码
#@param templateId 模板Id
#@param param 要传输的验证码
#@return 状态信息
def templateSMS(accountSid, accountToken, appId, toNumbers, templateId, param, isUseJson):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    signature = getSig(accountSid, accountToken, timestamp)
    url = "https://api.ucpaas.com" + ":" + "" + "/" + "2014-06-30" + \
        "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
    if isUseJson == True:
        body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}' % (
            appId, toNumbers, templateId, param)
        responseMode = "json"
    else:
        body = "<?xml version='1.0' encoding='utf-8'?>\
                <templateSMS>\
                    <appId>%s</appId>\
                    <to>%s</to>\
                    <templateId>%s</templateId>\
                    <param>%s</param>\
                </templateSMS>\
                " % (appId, toNumbers, templateId, param)
        responseMode = "xml"
    req = urllib2.Request(url)
    return urlOpen(createHttpReq(req, url, accountSid, timestamp, responseMode, body))


#在注册页面调用发送手机验证码
#@return 发送的验证码
@csrf_exempt
def getPhoneVerification(request):
    req = simplejson.load(request)
    user = User.objects.filter(username=req['phoneNum'])
    if len(user) != 0:
        response = JsonResponse({'verification': 'exist'})
        return response
    toNumber = req['phoneNum']
    seed = "1234567890"
    verification = []
    for i in range(4):
        verification.append(random.choice(seed))
    param = ''.join(verification)
    templateId = "125493"
    accountSid = "63e0b591e5197c7d5175f50a3a56587e"
    accountToken = "af87f23e566239b56b3e01e744f47c81"
    appId = "4e7193662d374d97963b6a40875127de"
    print(templateSMS(accountSid, accountToken,
                      appId, toNumber, templateId, param, True))
    response = JsonResponse({'verification': param})
    return response


@csrf_exempt
def getPhoneRand(request):
    req = simplejson.load(request)
    user = User.objects.filter(username=req['phoneNum'])
    if len(user) == 0:
        response = JsonResponse({'verification': 'none'})
        return response
    toNumber = req['phoneNum']
    seed = "1234567890"
    verification = []
    for i in range(4):
        verification.append(random.choice(seed))
    param = ''.join(verification)
    templateId = "125493"
    accountSid = "63e0b591e5197c7d5175f50a3a56587e"
    accountToken = "af87f23e566239b56b3e01e744f47c81"
    appId = "4e7193662d374d97963b6a40875127de"
    print(templateSMS(accountSid, accountToken,
                      appId, toNumber, templateId, param, True))
    response = JsonResponse({'verification': param})
    return response
