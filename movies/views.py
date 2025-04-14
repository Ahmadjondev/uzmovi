from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.urls import reverse
from .models import Category, Genre, Video, Episode, Comment
from .forms import CommentForm
from django.core.paginator import Paginator


def home(request):
    featured_videos = Video.objects.filter(is_featured=True)[:6]
    latest_movies = Video.objects.filter(content_type='movie').order_by('-created_at')[:6]
    latest_series = Video.objects.filter(content_type='series').order_by('-created_at')[:6]
    latest_cartoons = Video.objects.filter(content_type='cartoon').order_by('-created_at')[:6]
    popular_videos = Video.objects.filter(is_popular=True)[:6]

    context = {
        'featured_videos': featured_videos,
        'latest_movies': latest_movies,
        'latest_series': latest_series,
        'latest_cartoons': latest_cartoons,
        'popular_videos': popular_videos,
    }
    return render(request, 'movies/home.html', context)


class VideoListView(ListView):
    model = Video
    template_name = 'movies/video_list.html'
    context_object_name = 'videos'
    paginate_by = 18

    def get_queryset(self):
        content_type = self.kwargs.get('content_type', None)
        queryset = Video.objects.all()

        if content_type:
            queryset = queryset.filter(content_type=content_type)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = self.kwargs.get('content_type', None)

        if content_type:
            context['content_type'] = content_type
            if content_type == 'movie':
                context['title'] = 'Movies'
            elif content_type == 'series':
                context['title'] = 'TV Series'
            elif content_type == 'cartoon':
                context['title'] = 'Cartoons'
            elif content_type == 'clip':
                context['title'] = 'Clips'
        else:
            context['title'] = 'All Videos'

        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = 'movies/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()

        # Increment view count
        video.increment_views()
        # Get similar videos based on genres - optimize the query
        video_genres_ids = video.genres.values_list('id', flat=True)
        similar_videos = Video.objects.filter(
            genres__id__in=video_genres_ids
        ).exclude(
            id=video.id
        ).distinct().order_by('-views_count')[:6]

        # Get comments with prefetch for optimization
        comments = video.comments.filter(
            parent=None
        ).select_related('user').prefetch_related('likes', 'dislikes')

        context.update({
            'similar_videos': similar_videos,
            'comments': comments,
            'comment_form': CommentForm(),
        })

        # For series, get episodes grouped by season
        if video.content_type == 'series':
            episodes = video.episodes.all().order_by('season_number', 'episode_number')
            seasons = {}
            for episode in episodes:
                if episode.season_number not in seasons:
                    seasons[episode.season_number] = []
                seasons[episode.season_number].append(episode)

            context['seasons'] = seasons
        return context


class EpisodeDetailView(DetailView):
    model = Episode
    template_name = 'movies/episode_detail.html'
    context_object_name = 'episode'

    def get_object(self):
        series_slug = self.kwargs.get('series_slug')
        season = self.kwargs.get('season')
        episode = self.kwargs.get('episode')

        series = get_object_or_404(Video, slug=series_slug, content_type='series')
        episode_obj = get_object_or_404(Episode, series=series, season_number=season, episode_number=episode)

        # Increment view count
        episode_obj.increment_views()

        return episode_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episode = self.get_object()
        series = episode.series

        # Get all episodes for this series
        all_episodes = series.episodes.all()

        # Get next and previous episodes
        next_episode = all_episodes.filter(
            Q(season_number=episode.season_number, episode_number__gt=episode.episode_number) |
            Q(season_number__gt=episode.season_number)
        ).order_by('season_number', 'episode_number').first()

        prev_episode = all_episodes.filter(
            Q(season_number=episode.season_number, episode_number__lt=episode.episode_number) |
            Q(season_number__lt=episode.season_number)
        ).order_by('-season_number', '-episode_number').first()

        # Get comments
        comments = episode.comments.filter(parent=None)

        # Group episodes by season
        seasons = {}
        for ep in all_episodes:
            if ep.season_number not in seasons:
                seasons[ep.season_number] = []
            seasons[ep.season_number].append(ep)

        context['series'] = series
        context['seasons'] = seasons
        context['next_episode'] = next_episode
        context['prev_episode'] = prev_episode
        context['comments'] = comments
        context['comment_form'] = CommentForm()

        return context


@login_required
def add_comment(request, slug=None, series_slug=None, season=None, episode=None):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            # Determine if comment is for video or episode
            if slug:
                video = get_object_or_404(Video, slug=slug)
                comment.video = video
                redirect_url = reverse('video_detail', kwargs={'slug': slug})
            elif series_slug and season and episode:
                series = get_object_or_404(Video, slug=series_slug, content_type='series')
                episode_obj = get_object_or_404(Episode, series=series, season_number=season, episode_number=episode)
                comment.episode = episode_obj
                redirect_url = reverse('episode_detail', kwargs={
                    'series_slug': series_slug,
                    'season': season,
                    'episode': episode
                })

            # Handle reply to comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id

            comment.save()
            messages.success(request, 'Your comment has been added.')

            return redirect(redirect_url)

    return redirect('home')


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Toggle like
    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True
        # Remove dislike if exists
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)

    # Return JSON response for AJAX
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.get_likes_count(),
        'dislikes_count': comment.get_dislikes_count()
    })


@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Toggle dislike
    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
        disliked = False
    else:
        comment.dislikes.add(user)
        disliked = True
        # Remove like if exists
        if user in comment.likes.all():
            comment.likes.remove(user)

    # Return JSON response for AJAX
    return JsonResponse({
        'disliked': disliked,
        'likes_count': comment.get_likes_count(),
        'dislikes_count': comment.get_dislikes_count()
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    videos = Video.objects.filter(categories=category)

    context = {
        'category': category,
        'videos': videos,
    }

    return render(request, 'movies/category_detail.html', context)


def search(request):
    query = request.GET.get('q', '')
    genre_filter = request.GET.getlist('genre')
    content_type = request.GET.get('content_type', '')

    videos = Video.objects.all()

    # Apply search query
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query)
        )

    # Apply content type filter
    if content_type:
        videos = videos.filter(content_type=content_type)

    # Apply genre filter
    if genre_filter:
        videos = videos.filter(genres__name__in=genre_filter).distinct()

    # Get all genres for the filter sidebar
    genres = Genre.objects.all()

    # Pagination
    paginator = Paginator(videos, 18)  # Show 18 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'videos': page_obj,
        'query': query,
        'genres': genres,
        'selected_genres': genre_filter,
        'content_type': content_type,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
        'paginator': paginator,
    }

    return render(request, 'movies/search.html', context)


def ajax_search(request):
    query = request.GET.get('q', '')
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    videos = Video.objects.filter(
        Q(title__icontains=query) |
        Q(cast__icontains=query)
    )[:5]

    results = []
    for video in videos:
        results.append({
            'id': video.id,
            'title': video.title,
            'poster': video.get_poster_url(),
            'content_type': video.content_type,
            'url': video.get_absolute_url(),
        })

    return JsonResponse({'results': results})
