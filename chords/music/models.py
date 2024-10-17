from django.db import models
from django.utils.translation import gettext_lazy as _
from user_auth.models import User

class AllMusic(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=1024)
    music = models.FileField(upload_to='songs/audio/', blank=True)
    description = models.CharField(max_length=256)
    likes = models.IntegerField(default=0)
    love_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SeasonalCollectionsList(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='seasonalcollections/list/images/', blank=True)
    number_of_songs = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class SeasonalCollectionSongs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='seasonalcollection/images/', blank=True)
    songs = models.FileField(upload_to='seasonalcollections/songs/', blank=True)
    description = models.CharField(max_length=256)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class BeginnerFriendlyCollectionsList(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='beginnerfriendly/images/', blank=True)
    number_of_songs = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class BeginnerFriendlyCollectionSongs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='beginnerfriendly/images/', blank=True)
    songs = models.FileField(upload_to='beginnerfriendly/songs/', blank=True)
    description = models.CharField(max_length=256)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class SearchCollections(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='searchcollectionslist/images/', blank=True)
    likes = models.IntegerField(default=0)
    number_of_songs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class SearchCollectionsSongs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='searchcollections/images/', blank=True)
    description = models.CharField(max_length=256)
    songs = models.FileField(upload_to='searchcollections/songs/', blank=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class TrendingSongs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='trendingsongs/images/', blank=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    songs = models.FileField(upload_to='trending/songs/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class DiscoverNewSongs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='discover/images/', blank=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    songs = models.FileField(upload_to='discovernewsongs/songs/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TopArtistList(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='topartist/images/', blank=True)
    title = models.CharField(max_length=256)
    number_of_songs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ArtistSongs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='topartist/songs/images/', blank=True)
    title = models.CharField(max_length=256)
    songs = models.FileField(upload_to='topartist/songs/', blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ArtistProfile(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    image = models.ImageField(upload_to='topartist/profile/images/', blank=True)
    title = models.CharField(max_length=256)
    facebook_url = models.URLField(max_length=2000, blank=True, null=True)
    instagram_url = models.URLField(max_length=2000, blank=True, null=True)
    twitter_url = models.URLField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True)
    number_of_songs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    general_query = models.CharField(max_length=256)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Contribute(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=15)
    song_listing = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Support(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NewSong(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    song_name = models.CharField(max_length=256)
    artist_name = models.CharField(max_length=256)
    youtube_link = models.URLField(max_length=2000, blank=True, null=True)
    spotify_link = models.URLField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.song_name

class CreatePlayList(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    playlist_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True)  # Made blank=True for optional description
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.playlist_name
