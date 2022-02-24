from lib2to3.pytree import Base
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import BaseUserManager
# from django.conf import settings

class PlaylistPairs(models.Model):
    """Database Model for Playlist Pairs"""
    apple_music_token = models.CharField(max_length=128)
    spotify_music_token = models.CharField(max_length=128)
    apple_playlist_name = models.CharField(max_length=255)
    spotify_playlist_name = models.CharField(max_length=255)

    def get_apple_playlist_name(self):
        """Retieve the Apple playlist name"""
        return self.apple_playlist_name

    def get_apple_playlist_name(self):
        """Retieve the Spotify playlist name"""
        return self.spotify_playlist_name

    def __str__(self):
        """Return string representation of the PlaylistPairs object"""
        return "apple-" + self.apple_playlist_name + "_" + "spotify-" + self.spotify_playlist_name
