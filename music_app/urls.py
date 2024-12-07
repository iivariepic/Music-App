from django.urls import path
from . import views

app_name = 'music_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('albums/', views.album_list, name='album_list'),
    path('top_tracks/', views.top_tracks_list, name='top_tracks_list'),
    path('albums/<int:album_id>/tracks/', views.track_list, name='track_list'),
    path('<int:artist_id>/<int:album_id>/add_track/', views.add_track, name='add_track'),
    path('artist/', views.artist_list, name='artist_list'),
    path('artist/<int:artist_id>/albums/', views.artist_albums, name='artist_albums'),
    path('tracks/<int:track_id>/', views.track_details, name='track_details'),
    path('add_album/', views.add_album, name='add_album'),
    path('add_artist/', views.add_artist, name='add_artist'),
    path('add_review/<str:type>/<int:obj_id>', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('delete_album/<int:album_id>/', views.delete_album, name='delete_album'),
    path('delete_track/<int:track_id>/', views.delete_track, name='delete_track'),
    path('delete_artist/<int:artist_id>/', views.delete_artist, name='delete_artist'),
    path('edit_album/<int:album_id>/', views.edit_album, name='edit_album'),
    path('edit_track/<int:track_id>/', views.edit_track, name='edit_track'),
]