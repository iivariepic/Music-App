from django.shortcuts import render, get_object_or_404
from .models import Album, Track

def index(request):
    """Home page for music app"""
    return render(request, 'music_app/index.html')

def album_list(request):
    """View to display all albums"""
    albums = Album.objects.all()
    return render(request, 'music_app/albums.html', {'albums': albums})

def track_list(request, album_id):
    """View to display tracks from a specific album"""
    album = get_object_or_404(Album, id=album_id)
    tracks = Track.objects.filter(album=album)
    return render(request, 'music_app/tracks.html', {'tracks': tracks, 'album': album})