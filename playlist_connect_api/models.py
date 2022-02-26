from lib2to3.pytree import Base
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import BaseUserManager
# from django.conf import settings

class PlaylistPairs(models.Model):
    """Database Model for Playlist Pairs"""
    apple_token_1 = models.CharField(max_length=128)
    apple_token_2 = models.CharField(max_length=128)
    apple_token_3 = models.CharField(max_length=128)
    spotify_token_1 = models.CharField(max_length=128)
    spotify_token_2 = models.CharField(max_length=128)
    spotify_token_3 = models.CharField(max_length=128)
    apple_playlist_id = models.CharField(max_length=255)
    spotify_playlist_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def get_apple_playlist_id(self):
        """Retieve the Apple playlist name"""
        return self.apple_playlist_id

    def get_apple_playlist_id(self):
        """Retieve the Spotify playlist name"""
        return self.spotify_playlist_id

    def __str__(self):
        """Return string representation of the PlaylistPairs object"""
        return "apple-" + self.apple_playlist_id + "_" + "spotify-" + self.spotify_playlist_id
