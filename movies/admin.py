from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Genre, Video, Episode, Comment, Watchlist, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ('title', 'season_number', 'episode_number', 'video_url', 'duration', 'release_date')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'release_year', 'rating', 'views_count', 'is_featured', 'is_new_release')
    list_filter = ('content_type', 'is_featured', 'is_new_release', 'is_popular', 'categories', 'genres')
    search_fields = ('title', 'description', 'director', 'cast')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'genres')
    list_per_page = 25  # Limit items per page for better performance

    # Add raw_id_fields for better performance with many-to-many relationships
    raw_id_fields = ('categories', 'genres')
    inlines = [EpisodeInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'poster', 'poster_url', 'backdrop', 'backdrop_url')
        }),
        ('Video Source', {
            'fields': ('video_file', 'video_url')
        }),
        ('Details', {
            'fields': ('content_type', 'release_year', 'duration', 'rating', 'director', 'cast')
        }),
        ('Categories & Genres', {
            'fields': ('categories', 'genres', 'tags')
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_new_release', 'is_popular', 'views_count')
        }),
    )

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'series', 'season_number', 'episode_number', 'duration', 'views_count')
    list_filter = ('series', 'season_number')
    search_fields = ('title', 'description', 'series__title')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('series', 'title', 'slug', 'description')
        }),
        ('Episode Info', {
            'fields': ('season_number', 'episode_number', 'duration', 'release_date')
        }),
        ('Video Source', {
            'fields': ('video_file', 'video_url')
        }),
        ('Stats', {
            'fields': ('views_count',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('user', 'get_content_title', 'created_at', 'get_likes_count', 'get_dislikes_count')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content', 'video__title', 'episode__title')
    mptt_level_indent = 20

    def get_content_title(self, obj):
        if obj.video:
            return obj.video.title
        elif obj.episode:
            return obj.episode.title
        return "Unknown"
    get_content_title.short_description = 'Content'

    def get_likes_count(self, obj):
        return obj.get_likes_count()
    get_likes_count.short_description = 'Likes'

    def get_dislikes_count(self, obj):
        return obj.get_dislikes_count()
    get_dislikes_count.short_description = 'Dislikes'

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'video__title')
    date_hierarchy = 'added_at'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__username', 'video__title')
    date_hierarchy = 'created_at'
