import requests
from django.db import models


# Create your models here.


class Credential(models.Model):
    username = models.TextField(default="")
    password = models.TextField(default="")
    url = models.URLField(default="", null=True)




class Token(models.Model):
    access = models.TextField(default="")
    refresh = models.TextField(default="")

