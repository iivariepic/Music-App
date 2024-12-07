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


def add_track(request, artist_id, album_id):
    initial_data = {}
    if album_id != 0:  # Check if an album is provided
        album = get_object_or_404(Album, id=album_id)
        initial_data = {
            'album': album.id,
            'release_year': album.release_year,
        }

    """View to add a new track to a specific artist"""
    artist = get_object_or_404(Artist, id=artist_id)
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.artist = artist
            track.save()

            album = form.cleaned_data.get('album')
            if album is not None:  # Check if an album is selected
                return redirect('music_app:track_list', album_id=album.id)
            else:
                return redirect('music_app:artist_albums', artist_id=artist.id)

    else:
        form = TrackForm(initial=initial_data)
    return render(request, 'music_app/add_track.html', {'form': form, 'artist': artist})


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