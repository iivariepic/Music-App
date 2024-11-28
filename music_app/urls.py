from django.urls import path
from . import views

app_name = 'music_app'
urlpatterns=[
    #Home page
    path(' ',views.index, name='index'),
    path('albums/', views.album_list, name='album_list'),
     path('albums/<int:album_id>/tracks/', views.track_list, name='track_list'),

]