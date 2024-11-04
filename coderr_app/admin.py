from django.contrib import admin
from .models import UserProfile, Offers, OfferDetails, Orders, Reviews


class UserAdmin(admin.ModelAdmin):
    list_filter = ['user__username', 'location']
    list_display = ['user__username', 'email', 'location']


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Offers)
admin.site.register(OfferDetails)
admin.site.register(Orders)
admin.site.register(Reviews)