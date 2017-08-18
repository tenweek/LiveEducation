# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Room(models.Model):
    teacher = models.ForeignKey('backend.User')
    room_name = models.CharField(max_length=100)
    student_num = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)


class RoomStudent(models.Model):
    room = models.ForeignKey('backend.Room')
    student = models.ForeignKey('backend.User')
    can_speak = models.BooleanField(default=True)
    can_watch = models.BooleanField(default=True)


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    name = models.CharField(default='', max_length=16, unique=True)
    user_img = models.FileField(upload_to='./frontend/static/cover/')
    user_file = models.FileField(upload_to='./frontend/static/ppt/')
    file_num = models.IntegerField(default=0)
# Create your models here.
