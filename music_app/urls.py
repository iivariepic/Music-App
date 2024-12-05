
from django.urls import path
from . import views

app_name = 'music_app'
urlpatterns = [
     # Home page
    path('', views.index, name='index'),

    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:album_id>/tracks/', views.track_list, name='track_list'),
    path('artist/', views.artist_list, name='artist_list'),  # Ensure this name matches
    path('artist/<int:artist_id>/albums/', views.artist_albums, name='artist_albums'),
    path('add_album/', views.add_album, name='add_album'),
]