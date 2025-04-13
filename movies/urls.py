from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/<str:content_type>/', views.VideoListView.as_view(), name='content_type_list'),
    path('video/<slug:slug>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('series/<slug:series_slug>/season/<int:season>/episode/<int:episode>/',
         views.EpisodeDetailView.as_view(), name='episode_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
    path('comment/add/<slug:slug>/', views.add_comment, name='add_comment_video'),
    path('comment/add/<slug:series_slug>/season/<int:season>/episode/<int:episode>/',
         views.add_comment, name='add_comment_episode'),
    path('comment/like/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('comment/dislike/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
]
