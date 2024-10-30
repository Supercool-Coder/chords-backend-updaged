from datetime import date
from email.policy import default
import logging
from rest_framework import serializers
from user_auth.models import User
from user_auth.serializers import UserInformationSerializer
from music.models import (
    AllMusic, 
    SeasonalCollectionSongs, 
    ContactUs, 
    Contribute, 
    Support, 
    NewSong, 
    CreatePlayList, 
    SeasonalCollectionsList,
    BeginnerFriendlyCollectionsList,
    BeginnerFriendlyCollectionSongs,
    SearchCollections,
    SearchCollectionsSongs,
    TrendingSongs,
    DiscoverNewSongs,
    TopArtistList,
    ArtistSongs,
    ArtistProfile,
)
import uuid
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from django.db import transaction

def generate_unique_code(model):
    while True:
        code = uuid.uuid4().hex[:12].upper()
        if not model.objects.filter(code=code).exists():
            return code

logger = logging.getLogger(__name__)

class BaseMusicSerializer(serializers.ModelSerializer):
    uuidTemp = uuid.uuid4().hex[:12].upper()
    code = serializers.CharField(max_length=24, default=uuidTemp, read_only=True)

    def create(self, validated_data):
        validated_data['code'] = generate_unique_code(self.Meta.model)
        return super().create(validated_data)
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request is not None:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_music_url(self, obj):
        request = self.context.get('request')
        if obj.music and request is not None:
            return request.build_absolute_uri(obj.music.url)
        return None


class AllMusicSerializer(BaseMusicSerializer):
    name = serializers.CharField(max_length=1024)
    music = serializers.FileField()
    description = serializers.CharField(max_length=256)
    likes = serializers.IntegerField(default=0)
    love_by = serializers.IntegerField(default=0)

    class Meta:
        model = AllMusic
        fields = '__all__'

class SeasonalCollectionsListSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    number_of_songs = serializers.IntegerField()
    likes = serializers.IntegerField()

    class Meta:
        model = SeasonalCollectionsList
        fields = '__all__'

class SeasonalCollectionSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    songs = serializers.FileField()
    description=serializers.CharField(max_length=256)
    likes=serializers.IntegerField()

    class Meta:
        model = SeasonalCollectionSongs
        fields = '__all__'


class BeginnerFriendlyCollectionsListSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    number_of_songs = serializers.IntegerField()
    likes = serializers.IntegerField()

    class Meta:
        model = BeginnerFriendlyCollectionsList
        fields = '__all__'

class BeginnerFriendlyCollectionsSongsSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    songs = serializers.FileField()
    description = serializers.CharField(max_length=256)
    likes = serializers.IntegerField()

    class Meta:
        model = BeginnerFriendlyCollectionSongs
        fields = '__all__'

class SearchCollectionsSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    likes = serializers.IntegerField()
    number_of_songs = serializers.IntegerField()

    class Meta:
        model = SearchCollections
        fields = '__all__'

class SearchCollectionsSongsSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    description = serializers.CharField(max_length=256)
    songs = serializers.FileField()
    likes = serializers.IntegerField()

    class Meta:
        model = SearchCollectionsSongs
        fields = '__all__'

class TrendingSongsSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=256)
    songs = serializers.FileField()

    class Meta:
        model = TrendingSongs
        fields = '__all__'

class DiscoverSongsSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=256)
    songs = serializers.FileField()

    class Meta:
        model =DiscoverNewSongs
        fields = '__all__'

class TopArtistListSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=256)
    number_of_songs = serializers.IntegerField()

    class Meta:
        model = TopArtistList
        fields = '__all__'

class ArtistSongsSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=256)
    songs = serializers.FileField()
    views = serializers.IntegerField()
    likes = serializers.IntegerField()
    description = serializers.CharField(max_length=256)

    class Meta:
        model = ArtistSongs
        fields = '__all__'

class ArtistProfileSerializer(BaseMusicSerializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=256)
    number_of_songs = serializers.IntegerField()
    facebook_url = serializers.URLField(max_length=2000)
    instagram_url = serializers.URLField(max_length=2000)
    twitter_url = serializers.URLField(max_length=2000)
    description = serializers.CharField(max_length=256)

    class Meta:
        model = ArtistProfile
        fields = '__all__'

class ContactUsSerializer(BaseMusicSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=254)
    general_query = serializers.CharField(max_length=256)
    message = serializers.CharField()

    class Meta:
        model = ContactUs
        fields = '__all__'

class ContributeSerializer(BaseMusicSerializer):
    name = serializers.CharField(max_length=256)
    phone = serializers.CharField(max_length=15)
    song_listing = serializers.CharField(max_length=256)

    class Meta:
        model = Contribute
        fields = '__all__'

class SupportSerializer(BaseMusicSerializer):
    name = serializers.CharField(max_length=256)
    email = serializers.EmailField(max_length=254)
    message = serializers.CharField()

    class Meta:
        model = Support
        fields = '__all__'

class NewSongSerializer(BaseMusicSerializer):
    song_name = serializers.CharField(max_length=256)
    artist_name = serializers.CharField(max_length=256)
    youtube_link = serializers.URLField(max_length=2000, required=False)
    spotify_link = serializers.URLField(max_length=2000, required=False, allow_null=True)

    class Meta:
        model = NewSong
        fields = '__all__'

class PlayListSerializer(BaseMusicSerializer):
    playlist_name = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=256)

    class Meta:
        model = CreatePlayList
        fields = '__all__'
