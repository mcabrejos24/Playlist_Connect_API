from playlist_connect_api import sync
from playlist_connect_api import models

def sync_all_playlists():
    """Runs the sync function on all playlists in the database"""

    for obj in models.PlaylistPairs.objects.all().iterator():
        [apple_response, spotify_response] = sync.StartSync.sync(obj);
        print({'spotify_response': str(spotify_response), 'apple_response': str(apple_response)})
