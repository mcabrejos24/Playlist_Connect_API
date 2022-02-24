from rest_framework import serializers
from playlist_connect_api import models

class PlaylistPairsSerializer(serializers.ModelSerializer):
    """Serializes Playlist Pairs"""

    class Meta:
        model = models.PlaylistPairs
        fields = ('id', 'apple_music_token', 'spotify_music_token', 'apple_playlist_name', 'spotify_playlist_name')
        extra_kwargs = {'apple_music_token': {'read_only': True}, 'spotify_music_token': {'read_only': True}}
        