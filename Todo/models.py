
# Create your tests here.
#https://testdriven.io/blog/django-custom-user-model/
from django.db import models
from django.contrib.auth.models import User
import os


class TodoModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    todos = models.CharField(max_length=20 ,blank=True)
#  with AbstractUser we can inherit the feature of User Model from djnago Amdin

    def __str__(self):
        return f"User {self.user}"





