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
            # name = serializer.validated_data.get('name')
            # message = f'Hello {name}!'
            [response_apple, response_spotify] = sync.StartSync.sync(models.PlaylistPairs.objects.get(pk=serializerResponse.pk));
            print(response_apple, response_spotify)
            return Response({'message': 'sucessful!'})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
