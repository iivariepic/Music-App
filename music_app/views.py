from PyInstaller.utils.win32.winresource import add_or_update_resource
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from .models import Album, Track, Artist, Review
from .forms import AlbumForm, TrackForm, ArtistForm, ReviewForm


def filter_reviews(request, target_object):
    # Get the ContentType for the model
    object_content_type = ContentType.objects.get_for_model(target_object)

    if request.user.is_authenticated:
        # Show all public reviews and the user's own private review
        reviews = Review.objects.filter(
            content_type=object_content_type,
            object_id=target_object.id
        ).filter(
            Q(is_public=True) | Q(creator=request.user)
        ).distinct()

        # Separate user's own review
        user_review = reviews.filter(creator=request.user).first()
        if user_review:
            reviews = [user_review] + list(reviews.exclude(id=user_review.id))
    else:
        # Show only public reviews for unauthenticated users
        reviews = Review.objects.filter(
            content_type=object_content_type,
            object_id=target_object.id,
            is_public=True
        )

    return reviews

def sort_by_score(things:QuerySet):
    """Function to sort albums or tracks by score"""
    result = list(things)
    for thing in result:
        for other_thing in result:
            if other_thing != thing:
                if thing.get_avg_score() > other_thing.get_avg_score():
                    original_idx = result.index(thing)
                    other_idx = result.index(other_thing)
                    result.insert(other_idx, result.pop(original_idx))
                    break

    return result

def index(request):
    """Home page for music app"""
    return render(request, 'music_app/index.html')

def album_list(request):
    """View to display all albums and sort them by score"""
    # Retrieve all albums and order them by score
    albums = sort_by_score(Album.objects.all())

    return render(request, 'music_app/albums.html', {'albums': albums})

def top_tracks_list(request):
    """View to display all albums and sort them by score"""
    # Retrieve all albums and order them by score
    tracks = sort_by_score(Track.objects.all())

    return render(request, 'music_app/top_rated_tracks.html', {'tracks': tracks})

def track_list(request, album_id):
    """View to display tracks from a specific album"""
    album = get_object_or_404(Album, id=album_id)
    tracks = Track.objects.filter(album=album)

    # Filter reviews for the album
    reviews = filter_reviews(request, album)

    return render(request, 'music_app/tracks.html', {
        'tracks': tracks,
        'album': album,
        'reviews': reviews,
    })

@login_required
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

def track_details(request, track_id):
    """View to display specific track details"""
    track = get_object_or_404(Track, id=track_id)
    reviews = filter_reviews(request, track)
    return render(request, 'music_app/track_details.html',
                  {'track': track, 'reviews': reviews})


@login_required
def add_track(request, artist_id, album_id):
    """View to add a new track to a specific artist"""

    initial_data = {}
    if album_id != 0:  # Check if an album is provided
        album = get_object_or_404(Album, id=album_id)
        initial_data.update({
            'album': album.id,
            'release_year': album.release_year,
        })

    artist = get_object_or_404(Artist, id=artist_id)
    if request.method == 'POST':
        form = TrackForm(request.POST, artist=artist)
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
        form = TrackForm(initial=initial_data, artist=artist)
    return render(request, 'music_app/add_track.html', {'form': form, 'artist': artist})


@login_required
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


@login_required
def add_review(request, type, obj_id):
    """View to add a new artist"""

    if type=='album':
        object = get_object_or_404(Album, id=obj_id)
    else:
        object = get_object_or_404(Track, id=obj_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.content_type = ContentType.objects.get_for_model(object)
            review.object_id = object.id
            review.creator = request.user
            review.save()
            if type=='album':
                return redirect('music_app:track_list', album_id=obj_id)
            else:
                return redirect('music_app:track_details', track_id=object.id)
    else:
        form = ReviewForm()
    return render(request, 'music_app/add_review.html',
                  {'form': form, 'type': type, 'object': object})

def edit_review(request, review_id):
    """Edit an existing review"""
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.creator:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current review
        form = ReviewForm(instance=review)
    else:
        # POST data submitted, process data
        form = ReviewForm(instance=review, data=request.POST)
        if form.is_valid():
            form.save()
            if review.content_type == ContentType.objects.get_for_model(Album):
                return redirect('music_app:track_list', album_id=review.object_id)
            else:
                return redirect('music_app:track_details', track_id=review.object_id)

    context = {'review': review,
               'type': review.content_type.name.lower(),
               'object': get_object_or_404(review.content_type.model_class(),
                                           id=review.object_id),
               'form': form}
    return render(request, 'music_app/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Ensure the user is the creator of the review
    if request.user == review.creator:
        review.delete()  # Deletes the review
        if review.content_type == ContentType.objects.get_for_model(Album):
            return redirect('music_app:track_list', album_id=review.object_id)
        else:
            return redirect('music_app:track_details', track_id=review.object_id)
    else:
        # Optionally, show a message or redirect to an error page
        raise Http404