from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(Section)
