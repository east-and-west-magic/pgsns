from user.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib import admin

# Register your models here.




admin.site.register(CustomUser)
admin.site.unregister(Group)
