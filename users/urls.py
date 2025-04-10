from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.user_settings, name='user_settings'),
]
