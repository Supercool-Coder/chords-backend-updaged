from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from music.views import (
    AllMusicView,
    SeasonalCollectioSongsView,
    ContactUsView,
    ContributionsView,
    SupportView,
    NewSongView,
    PlayListView,
    SeasonalCollectionsListView,
    BeginnerFriendlyCollectionsListView,
    BeginnerFriendlyCollectionsSongsView,
    SearchCollectionsView,
    SearchCollectionsSongsView,
    TrendingSongsView,
    TopArtistsView,
    ArtistSongsView,
    ArtistProfileView,
    SelectedAllMusicListsView,
    SelectedSeasonalCollectionsListsView,
    SelectedTrendingCollectionsListsView,
    TopArtistCollectionsList,
    SearchAllMusicView,


)
urlpatterns = [
    # AllMusicView
    path('all-music', AllMusicView.as_view(), name='all-music'),
    path('all-music/<int:pk>',  AllMusicView.as_view(), name='all-music'),
    
    # NewSongView with CRUD operations
    path('new-song', NewSongView.as_view(), name='new-song-list-create'),
    path('new-song/<int:pk>', NewSongView.as_view(), name='new-song-detail'),

    # SeasonalCollectionsListView
    path('seasonal-collections-list', SeasonalCollectionsListView.as_view(), name='seasonal-collections-list'),
    path('seasonal-collections-list/<int:pk>', SeasonalCollectionsListView.as_view(), name='seasonal-collections-list'),
    
    # SeasonalCollectioSongsView
    path('seasonal-collection-songs', SeasonalCollectioSongsView.as_view(), name='seasonal-collection-songs'),
    path('seasonal-collection-songs/<int:pk>', SeasonalCollectioSongsView.as_view(), name='seasonal-collection-songs'),

    # PlayListView with CRUD operations
    path('playlist', PlayListView.as_view(), name='playlist-list-create'),
    path('playlist/<int:pk>', PlayListView.as_view(), name='playlist-detail'),
    
    # BeginnerFriendlyCollectionsListView
    path('beginner-friendly-collections-list', BeginnerFriendlyCollectionsListView.as_view(), name='beginner-friendly-collections-list'),
    path('beginner-friendly-collections-list/<int:pk>', BeginnerFriendlyCollectionsListView.as_view(), name='beginner-friendly-collections-list'),
    
    # BeginnerFriendlyCollectionsSongsView with CRUD operations
    path('beginner-friendly-collection-songs', BeginnerFriendlyCollectionsSongsView.as_view(), name='beginner-friendly-collection-songs'),
    path('beginner-friendly-collection-songs/<int:pk>', BeginnerFriendlyCollectionsSongsView.as_view(), name='beginner-friendly-collection-songs'),

    # SearchCollectionsView
    path('search-collections-list', SearchCollectionsView.as_view(), name='search-collections-list'),
    path('search-collections-list/<int:pk>', SearchCollectionsView.as_view(), name='search-collections-list'),
    
    # SearchCollectionsSongsView with CRUD operations
    path('search-collections-songs', SearchCollectionsSongsView.as_view(), name='search-collections-songs'),
    path('search-collections-songs/<int:pk>', SearchCollectionsSongsView.as_view(), name='search-collections-songs'),

    # TrendingSongsView
    path('trending-songs', TrendingSongsView.as_view(), name='trending-songs'),
    path('trending-songs/<int:pk>', TrendingSongsView.as_view(), name='trending-songs'),
    
    # DiscoverSongsView (assuming it’s the same as TrendingSongsView for now)
    path('discover-songs', TrendingSongsView.as_view(), name='discover-songs'),  # Update if a different view is used
    path('discover-songs/<int:pk>', TrendingSongsView.as_view(), name='discover-songs'),  # Update if a different view is used
    
    # TopArtistListView
    path('top-artist-list', TopArtistsView.as_view(), name='top-artist-list'),
    path('top-artist-list/<int:pk>', TopArtistsView.as_view(), name='top-artist-list'),
    
    # ArtistSongsView
    path('artist-songs', ArtistSongsView.as_view(), name='artist-songs'),
    path('artist-songs/<int:pk>', ArtistSongsView.as_view(), name='artist-songs'),
    
    # ArtistProfileView
    path('artist-profile', ArtistProfileView.as_view(), name='artist-profile'),
    path('artist-profile/<int:pk>', ArtistProfileView.as_view(), name='artist-profile'),
    
    # ContactUsView with CRUD operations
    path('contact-us', ContactUsView.as_view(), name='contact-us-list-create'),
    path('contact-us/<int:pk>', ContactUsView.as_view(), name='contact-us-detail'),
    
    # ContributeView
    path('contribute', ContributionsView.as_view(), name='contribute'),
    path('contribute/<int:pk>', ContributionsView.as_view(), name='contribute'),
    
    # SupportView with CRUD operations
    path('support', SupportView.as_view(), name='support-list-create'),
    path('support/<int:pk>', SupportView.as_view(), name='support-detail'),


    path('selected-all-music-list/', SelectedAllMusicListsView.as_view(), name='music-list'),  # Updated path
    path('selected-seasonal-collections-list/', SelectedSeasonalCollectionsListsView.as_view(), name='seasonal-collection-list'),
    path('selected-trending-songs-list/', SelectedTrendingCollectionsListsView.as_view(), name='seasonal-collection-list'),
    path('selected-trending-songs-list/', TopArtistCollectionsList.as_view(), name='seasonal-collection-list'),

    path('search-all-music', SearchAllMusicView.as_view(), name='all-music'),


] 
