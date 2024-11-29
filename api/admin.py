from django.contrib import admin
from .models import UserData

class UserDataAdminPanel(admin.ModelAdmin):
    model = UserData
    list_display = ['uid', 'passwords']

admin.site.register(UserData, UserDataAdminPanel)

# Register your models here.
