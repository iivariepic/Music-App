from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import datetime


class Artist(models.Model):
    """A model for artists"""
    name = models.CharField(max_length=100)

    def __str__(self):
        """Return string representation of Artist"""
        return self.name

    def get_singles(self):
        """Method to get all singles (albumless songs) from an artist"""
        return Track.objects.filter(artist=self, album__isnull=True)



class Album(models.Model):
    """A model for albums"""
    name = models.CharField(max_length=300)
    release_year = models.IntegerField(default=1900,
                    validators=[
                        MaxValueValidator(datetime.datetime.now().year),
                        MinValueValidator(1900)])

    date_added = models.DateField(auto_now_add=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the Album"""
        return self.name + " - " + self.artist.name

    def get_avg_score(self):
        """Method to get average score of album"""
        reviews = Review.objects.filter(
            content_type= ContentType.objects.get_for_model(self),
            object_id=self.id)
        if len(reviews) == 0:
            return 0
        else:
            combined_sum = 0
            for review in reviews:
                combined_sum += review.rating
            return combined_sum / len(reviews)



class Track(models.Model):
    """A model for tracks/songs"""
    name = models.CharField(max_length=300)
    length = models.IntegerField(default=0) # Length in seconds
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    # Song can be a single that is not on an album as well
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)

    release_year = models.IntegerField(default=1900,
                                       validators=[
                                           MaxValueValidator(datetime.datetime.now().year),
                                           MinValueValidator(1900)
                                       ])

    def __str__(self):
        return self.name + " | " + self.artist.name

    def get_length(self):
        minutes = self.length // 60
        seconds = self.length % 60
        result = f"{minutes}:{seconds:02}"
        return result

    def get_avg_score(self):
        """Method to get average score of track"""
        reviews = Review.objects.filter(
            content_type= ContentType.objects.get_for_model(self),
            object_id=self.id)
        if len(reviews) == 0:
            return 0
        else:
            combined_sum = 0
            for review in reviews:
                combined_sum += review.rating
            return combined_sum / len(reviews)


class Review(models.Model):
    """A model for reviews of a track or an album"""
    # Fields for the Generic Foreign Key (these have to be defined when creating a review)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Song or album?
    object_id = models.PositiveIntegerField() # ID of song or album
    target_object = GenericForeignKey('content_type', 'object_id')

    # Additional fields
    content = models.TextField()
    rating = models.IntegerField(default=0,
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(0),
                                ])
    date_created = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=False) # Public means other users can see this review
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of a Review"""
        result = f"Stars: {self.rating}"
        result += f" | {self.creator}\n"
        result += f"{self.content[:50]}"
        if len(self.content) > 50:
            result += "..."

        return result