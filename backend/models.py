# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Room(models.Model):
    teacher = models.ForeignKey('backend.User')
    roomName = models.CharField(max_length=100)
    studentNum = models.IntegerField(default=0)
    createTime = models.DateTimeField(default=timezone.now)


class RoomStudent(models.Model):
    room = models.ForeignKey('backend.Room')
    student = models.ForeignKey('backend.User')


class StuBlackList(models.Model):
    room = models.ForeignKey('backend.Room')
    student = models.ForeignKey('backend.User')


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    name = models.CharField(default='', max_length=16)
# Create your models here.
