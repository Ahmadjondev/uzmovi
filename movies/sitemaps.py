from django.contrib.sitemaps import Sitemap
from .models import Category, Video, Episode
from django.urls import reverse

class StaticSitemap(Sitemap):

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

class VideoSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
    def location(self, obj):
        return obj.get_absolute_url()

class EpisodeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Episode.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()
