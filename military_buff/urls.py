from django.urls import path
from military_buff import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games, name='games'),
    path('books/', views.books, name='books'),
    path('fetch_books/<int:timeperiod_id>/<int:region_id>/', views.fetch_books, name='fetch_books'),
    path('fetch_games/<int:timeperiod_id>/<int:region_id>/',views.fetch_games,name='fetch_games'),
    path( "videos/",views.videos_page, name="videos"),
    path("fetch_video_playlists/<int:timeperiod_id>/<int:region_id>/",views.fetch_video_playlists,name="fetch_video_playlists"),
    path("fetch_playlist_videos/<int:playlist_id>/", views.fetch_playlist_videos,  name="fetch_playlist_videos"),
]
