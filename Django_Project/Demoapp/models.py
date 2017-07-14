# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    Mobile = models.CharField(max_length=255) #2update Mobile = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)