from django.contrib import admin

from .models import Client

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


admin.site.register(Client)
