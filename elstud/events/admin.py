from django.contrib import admin


# Register your models here.
from events.models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'address', 'type', 'image', 'time_start', 'time_end', 'description']


admin.site.register(Event, EventAdmin)