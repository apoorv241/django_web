from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Region, TimePeriod, Book , Game  ,VideoPlaylist, Video
from django.db.models import Count
from django.shortcuts import get_object_or_404 
from django.views.decorators.http import require_GET
# Create your views here.

@require_GET
def home(request):
    return render(request, 'military_buff/home.html')

@require_GET
def books(request):
    regions = Region.objects.all()
    time_periods = TimePeriod.objects.all()
    context = {
        'regions': regions,
        'time_periods': time_periods
    }
    return render(request, 'military_buff/books.html',context)

@require_GET
def games(request):
    regions = Region.objects.all()
    time_periods = TimePeriod.objects.all()
    context = {
        'regions': regions,
        'time_periods': time_periods
    }
    return render(request, 'military_buff/games.html',context)

@require_GET
def fetch_books(request, timeperiod_id, region_id):

    books = Book.objects.filter(
        timeperiod_id=timeperiod_id,
        region_id=region_id
    ).values(
        'id',
        'name',
        'author',
        'photo_url',
        'review',
        'about_the_author',
        'buy_url',
    )

    return JsonResponse({
        'books': list(books)
    })



@require_GET
def fetch_games(request, timeperiod_id, region_id):

    games = Game.objects.filter(
        timeperiod_id=timeperiod_id,
        region_id=region_id
    ).values(
        'id',
        'name',
        'photo_url',
        'review',
        'about_the_game',
        'website_url',
    )

    return JsonResponse({
        'games': list(games)
    })
    
@require_GET
def videos_page(request):

    context = {
        "time_periods": TimePeriod.objects.all(),
        "regions": Region.objects.all()
    }

    return render(
        request,
        "military_buff/videos.html",
        context
    )


# AJAX 1: Get playlists by region and time period
@require_GET
def fetch_video_playlists(request, timeperiod_id, region_id):

    playlists = VideoPlaylist.objects.filter(
        timeperiod_id=timeperiod_id,
        region_id=region_id
    ).annotate(
        video_count=Count("videos")
    ).values(
        "id",
        "name",
        "about",
        "video_count"
    ).order_by("name")

    return JsonResponse({
        "playlists": list(playlists)
    })


# AJAX 2: Get videos belonging to the selected playlist
@require_GET
def fetch_playlist_videos(request, playlist_id):

    playlist = get_object_or_404(
        VideoPlaylist,
        id=playlist_id
    )

    videos = Video.objects.filter(
        playlist=playlist
    ).order_by(
        "episode_number",
        "id"
    ).values(
        "id",
        "title",
        "url",
        "transcript",
        "about_the_video",
        "thumbnail_url",
        "episode_number"
    )

    return JsonResponse({
        "playlist": playlist.name,
        "videos": list(videos)
    })
