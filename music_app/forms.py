from django import forms
from .models import Album, Track

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'release_year', 'artist']



class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['name', 'length', 'artist', 'album']