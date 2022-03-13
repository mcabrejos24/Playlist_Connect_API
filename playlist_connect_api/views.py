from rest_framework import viewsets
from rest_framework.response import Response
from playlist_connect_api import serializers
from rest_framework import status
from playlist_connect_api import models

from playlist_connect_api import sync


class PlaylistPairsViewSet(viewsets.ModelViewSet):
    """Handles creating playlist pairs"""
    serializer_class = serializers.PlaylistPairsSerializer
    queryset = models.PlaylistPairs.objects.all();

    def create(self, request):
        """Create a new hello message"""
        modelData = request.data
        serializer = self.serializer_class(data=modelData)

        if serializer.is_valid():
            serializerResponse = serializer.save()
            [apple_response, spotify_response] = sync.StartSync.sync(models.PlaylistPairs.objects.get(pk=serializerResponse.pk));
            print(apple_response, spotify_response)
            if apple_response == 0 or spotify_response == 0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'spotify_response': str(spotify_response), 'apple_response': str(apple_response)})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
