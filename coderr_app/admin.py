from django.contrib import admin
from .models import UserProfile


class UserAdmin(admin.ModelAdmin):
    list_filter = ['user__username', 'location']
    list_display = ['user__username', 'email', 'location']


admin.site.register(UserProfile, UserAdmin)