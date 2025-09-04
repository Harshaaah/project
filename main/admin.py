# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Client
# from .models import Counsellor,Booking

# admin.site.register(Client)
# admin.site.register(Counsellor)
# admin.site.register(Booking)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Counsellor, Booking

admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Counsellor)
admin.site.register(Booking)