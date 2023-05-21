from django.contrib import admin


# Register your models here.
from events.models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'address', 'type', 'image', 'time', 'description']


admin.site.register(Event, EventAdmin)