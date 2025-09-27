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

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'counsellor', 'get_status_display', 'approved_date', 'approved_time', 'requested_at')
    list_filter = ('status', 'approved_date', 'counsellor')
    search_fields = ('client__user__username', 'counsellor__user__username')
    ordering = ('-requested_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Counsellor)
admin.site.register(Booking, BookingAdmin)
