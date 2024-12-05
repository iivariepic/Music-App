from django.urls import path
from . import views

app_name = 'music_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    path('albums/', views.album_list, name='album_list'),
    path('add_album/', views.add_album, name='add_album'),
    path('artist/', views.artist_list, name='artist_list'),
    path('artist/<int:artist_id>/albums/', views.artist_albums, name='artist_albums'),
    path('artist/', views.artist, name='artist'),
]
