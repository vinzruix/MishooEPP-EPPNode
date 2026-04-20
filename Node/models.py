from django.db import models

# Create your models here.


class Node(models.Model):
    is_active = models.BooleanField(default=False)
    epp = models.TextField(null=True)




