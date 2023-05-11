from django.contrib import admin

# Register your models here.
from account.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_student', 'group', 'organization_name']
    list_editable = ['is_student', 'group', 'organization_name']


admin.site.register(UserProfile, UserProfileAdmin)