from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
        ('cartoon', 'Cartoon'),
        ('clip', 'Clip'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True, help_text="URL to poster image if not uploading")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="URL to video (YouTube, Vimeo, etc.)")
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    categories = models.ManyToManyField(Category, related_name='videos')
    genres = models.ManyToManyField(Genre, related_name='videos')
    cast = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Use the same view for all content types
        episodes = Episode.objects.filter(series=self)  # Check if this is a series
        if episodes.exists() or self.content_type == 'series':
            episode = episodes.first()
            return reverse('episode_detail', kwargs={
            'series_slug': episode.series.slug,
            'season': episode.season_number,
            'episode': episode.episode_number
        })
        return reverse('video_detail', kwargs={'slug': self.slug})

    def get_genres_display(self):
        return ', '.join([genre.name for genre in self.genres.all()])

    def get_cast_list(self):
        if self.cast:
            return [actor.strip() for actor in self.cast.split(',')]
        return []

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def get_poster_url(self):
        if self.poster and hasattr(self.poster, 'url'):
            return self.poster.url
        elif self.poster_url:
            return self.poster_url
        return '/static/img/placeholder-poster.jpg'

    def get_backdrop_url(self):
        return '/static/img/placeholder-backdrop.jpg'

    def get_embed_url(self):
        if not self.video_url:
            return None
        import re
        # YouTube
        if 'youtube.com/watch' in self.video_url or 'youtu.be/' in self.video_url:
            video_id = None
            if 'youtube.com/watch' in self.video_url:
                # Extract from youtube.com/watch?v=VIDEO_ID
                import re
                match = re.search(r'v=([^&]+)', self.video_url)
                if match:
                    video_id = match.group(1)
            elif 'youtu.be/' in self.video_url:
                # Extract from youtu.be/VIDEO_ID
                video_id = self.video_url.split('/')[-1]

            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'
        # OK.ru
        if 'ok.ru/video/' in self.video_url:
            match = re.search(r'ok\.ru/video/(\d+)', self.video_url)
            if match:
                video_id = match.group(1)
                return f'https://ok.ru/videoembed/{video_id}'

        # Vimeo
        if 'vimeo.com/' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://player.vimeo.com/video/{video_id}'

        # For other services or direct video URLs, return as is
        return self.video_url


class Episode(models.Model):
    series = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    episode_number = models.PositiveIntegerField()
    season_number = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='episodes/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="URL to video (YouTube, Vimeo, etc.)")
    poster_url = models.URLField(blank=True, null=True, help_text="URL to episode poster image")
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('series', 'season_number', 'episode_number')
        ordering = ['season_number', 'episode_number']

    def __str__(self):
        return f"{self.series.title} - S{self.season_number:02d}E{self.episode_number:02d} - {self.title}"

    def get_absolute_url(self):
        return reverse('episode_detail', kwargs={
            'series_slug': self.series.slug,
            'season': self.season_number,
            'episode': self.episode_number
        })
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def get_poster_url(self):
        if self.poster_url:
            return self.poster_url
        return self.series.get_poster_url()

    def get_embed_url(self):
        """Convert YouTube, Vimeo, etc. URLs to embed URLs"""
        if not self.video_url:
            return None

        # YouTube
        if 'youtube.com/watch' in self.video_url or 'youtu.be/' in self.video_url:
            video_id = None
            if 'youtube.com/watch' in self.video_url:
                # Extract from youtube.com/watch?v=VIDEO_ID
                import re
                match = re.search(r'v=([^&]+)', self.video_url)
                if match:
                    video_id = match.group(1)
            elif 'youtu.be/' in self.video_url:
                # Extract from youtu.be/VIDEO_ID
                video_id = self.video_url.split('/')[-1]

            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'
        # OK.ru
        import re
        if 'ok.ru/video/' in self.video_url:
            match = re.search(r'ok\.ru/video/(\d+)', self.video_url)
            if match:
                video_id = match.group(1)
                return f'https://ok.ru/videoembed/{video_id}'

        # Vimeo
        if 'vimeo.com/' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://player.vimeo.com/video/{video_id}'

        # For other services or direct video URLs, return as is
        return self.video_url


class Comment(MPTTModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

    def get_likes_count(self):
        return self.likes.count()

    def get_dislikes_count(self):
        return self.dislikes.count()