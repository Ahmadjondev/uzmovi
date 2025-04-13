from django import template
import random
from movies.models import Video

register = template.Library()

@register.filter
def random_video(content_type, exclude_id=None):
    """
    Returns a random video of the specified content type.
    Optionally excludes a video by ID.
    """
    videos = Video.objects.filter(content_type=content_type)
    if exclude_id:
        videos = videos.exclude(id=exclude_id)

    if not videos.exists():
        return None

    return random.choice(list(videos))
