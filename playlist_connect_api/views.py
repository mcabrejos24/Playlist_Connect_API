from playlist_connect_api import serializers
from rest_framework import viewsets

from playlist_connect_api import serializers
from playlist_connect_api import models

class PlaylistPairsViewSet(viewsets.ModelViewSet):
    """Handles creating playlist pairs"""
    serializer_class = serializers.PlaylistPairsSerializer
    queryset = models.PlaylistPairs.objects.all();
    