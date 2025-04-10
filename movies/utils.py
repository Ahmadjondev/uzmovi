from django.db.models import Count
from .models import Movie


def get_recommendations(movie, limit=6):
    """
    Get movie recommendations based on categories and actors
    """
    # Get movies with similar categories
    similar_categories = Movie.objects.filter(
        categories__in=movie.categories.all()
    ).exclude(id=movie.id)

    # Get movies with similar actors
    similar_actors = Movie.objects.filter(
        actors__in=movie.actors.all()
    ).exclude(id=movie.id)

    # Combine and rank by similarity
    similar_movies = similar_categories.union(similar_actors)

    # Count occurrences to rank by similarity
    similar_movies = similar_movies.annotate(
        similarity=Count('id')
    ).order_by('-similarity', '-release_date')

    return similar_movies[:limit]
