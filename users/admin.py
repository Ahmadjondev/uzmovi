from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'email_notifications')
    list_filter = ('dark_mode', 'email_notifications', 'favorite_genres')
    search_fields = ('user__username', 'user__email', 'bio')
    filter_horizontal = ('favorite_genres',)
