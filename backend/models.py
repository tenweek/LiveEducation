# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    isTeacher = models.BooleanField(default=False)
    name = models.CharField(default='', max_length=16)
# Create your models here.
