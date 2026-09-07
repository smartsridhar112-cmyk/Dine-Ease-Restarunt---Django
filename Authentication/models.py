from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField(null=True,default=0,blank=True)
    dateofbirth= models.DateField(null=True)
    role_choice= (
        ("Admin","Admin"),
        ("Manager","Manager"),
        ("Employee","Employee"),
        ("Customer","Customer"),
    )
    role=models.CharField(max_length=20,choices=role_choice,default="Customer") 