from django import forms
from .models import Album, Track,Artist

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'release_year', 'artist']



class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['name', 'length', 'album', 'release_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        artist = kwargs.pop('artist')
        self.fields['album'].empty_label = "None (Single)"  # Add an option for singles
        self.fields['album'].required = False  # Make the album field not required

        self.fields['album'].queryset = Album.objects.filter(artist=artist)


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name']