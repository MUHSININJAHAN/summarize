from django.db import models

# Create your models here.

class Registration(models.Model):
    ID = models.AutoField(primary_key = True)
    Name = models.CharField(blank=True, max_length=500, null=True)
    Email = models.CharField(blank=True, max_length=500, null=True, unique=True)
    Password = models.CharField(blank=True, max_length=500, null=True)