from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Track, Artist
from .forms import AlbumForm, TrackForm, ArtistForm


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

def add_album(request):
    """View to add a new album"""
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('music_app:album_list')
    else:
        form = AlbumForm()
    return render(request, 'music_app/add_album.html', {'form': form})

def artist_list(request):
    """View to display all artists"""
    artists = Artist.objects.all()
    return render(request, 'music_app/artist.html', {'artists': artists})

def artist_albums(request, artist_id):
    """View to display albums and singles of a specific artist"""
    artist = get_object_or_404(Artist, id=artist_id)
    albums = Album.objects.filter(artist=artist)
    singles = artist.get_singles()
    return render(request, 'music_app/artist_albums.html',
                  {'artist': artist, 'albums': albums,
                   'singles': singles})



def add_track(request, album_id):
    """View to add a new track to a specific album"""
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.album = album
            track.save()
            return redirect('music_app:track_list', album_id=album.id)
    else:
        form = TrackForm(initial={'album': album})
    return render(request, 'music_app/add_track.html', {'form': form, 'album': album})

def add_artist(request):
    """View to add a new artist"""
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('music_app:artist_list')
    else:
        form = ArtistForm()
    return render(request, 'music_app/add_artist.html', {'form': form})