from rest_framework import serializers
from playlist_connect_api import models

class PlaylistPairsSerializer(serializers.ModelSerializer):
    """Serializes Playlist Pairs"""

    class Meta:
        model = models.PlaylistPairs
        fields = ('id', 'apple_token_1', 'apple_token_2', 'apple_token_3', 'spotify_token_1', 'spotify_token_2', 'spotify_token_3', 'spotify_refresh_1', 'spotify_refresh_2', 'apple_playlist_id', 'spotify_playlist_id')
        # disables access to update db via ui, remove for access in development
        extra_kwargs = {'apple_token_1': {'read_only': True}, 'apple_token_2': {'read_only': True}, 'apple_token_3': {'read_only': True}, 'spotify_token_1': {'read_only': True}, 'spotify_token_2': {'read_only': True}, 'spotify_token_3': {'read_only': True}, 'spotify_refresh_1': {'read_only': True}, 'spotify_refresh_2': {'read_only': True}, 'apple_playlist_id': {'read_only': True}, 'spotify_playlist_id': {'read_only': True}}
