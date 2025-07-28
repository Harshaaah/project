from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client
from .models import Counsellor

admin.site.register(Client)
admin.site.register(Counsellor)