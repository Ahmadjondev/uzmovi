from django import template
from django.template.defaultfilters import register
from random import sample
from .models import Category, Video

@register.filter
def random_videos(content_type, count=6):
    """
    Return random videos of a specific content type
    """
    videos = Video.objects.filter(content_type=content_type)
    if videos.count() <= count:
        return videos
    return sample(list(videos), count)

def categories(request):
    """
    Add categories to context for all templates
    """
    return {
        'categories': Category.objects.all(),
        'random_videos': random_videos
    }
