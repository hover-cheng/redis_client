from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class redisInfo(models.Model):
    redisname = models.CharField(max_length=10, null=False, blank=False)
    type_list = (('Sentinel', 'Sentinel'),
                 ('Cluster', 'Cluster'),
                 ('Single', 'Single')
                 )
    redistype = models.CharField(choices=type_list, default=2, max_length=10)
    mastername = models.CharField(max_length=20, default='')
    nodelist = models.CharField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=32, default=None, null=True, blank=True)
    projectname = models.CharField(max_length=20, null=False, blank=False)
    director = models.CharField(max_length=10, null=True, blank=True)
    createtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.redisname


class operationlog(models.Model):
    redisname = models.CharField(max_length=100, null=False, blank=False)
    operation = models.CharField(max_length=100, null=False, blank=False)
    operator = models.CharField(max_length=20, null=False, blank=False)
    createtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.redisname


class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    userpermission = models.CharField(max_length=100, null=True, blank=True)
    belong_to = models.OneToOneField(to=User, related_name='userprofile')

    def __str__(self):
        return self.name
