from django.contrib import admin
from redisconect.models import redisInfo, operationlog, UserProfile

# Register your models here.
admin.site.register(redisInfo)
admin.site.register(operationlog)
admin.site.register(UserProfile)
