from django.urls import path
from . import views

app_name = 'music_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:album_id>/tracks/', views.track_list, name='track_list'),
    path('<int:artist_id>/add_track/', views.add_track, name='add_track'),
    path('artist/', views.artist_list, name='artist_list'),
    path('artist/<int:artist_id>/albums/', views.artist_albums, name='artist_albums'),
    path('add_album/', views.add_album, name='add_album'),
    path('add_artist/', views.add_artist, name='add_artist'),
]