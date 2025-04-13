from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications')
    # list_filter = ('email_notifications')
    search_fields = ('user__username', 'user__email')
    # filter_horizontal = ('favorite_genres',)
