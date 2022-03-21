from django.test import TestCase
from playlist_connect_api.models import PlaylistPairs


class PlaylistPairTestCase(TestCase):
    def setUp(self):
        PlaylistPairs.objects.create(
            apple_token_1="apple_token_1",
            apple_token_2="apple_token_2",
            apple_token_3="apple_token_3",
            spotify_token_1="spotify_token_1",
            spotify_token_2="spotify_token_2",
            spotify_token_3="spotify_token_3",
            spotify_refresh_1="spotify_refresh_1",
            spotify_refresh_2="spotify_refresh_2",
            apple_playlist_id="apple_playlist_id_1",
            spotify_playlist_id="spotify_playlist_id_1"
        )
        PlaylistPairs.objects.create(
            apple_token_1="apple_token_1",
            apple_token_2="apple_token_2",
            apple_token_3="apple_token_3",
            spotify_token_1="spotify_token_1",
            spotify_token_2="spotify_token_2",
            spotify_token_3="spotify_token_3",
            spotify_refresh_1="spotify_refresh_1",
            spotify_refresh_2="spotify_refresh_2",
            apple_playlist_id="apple_playlist_id_2",
            spotify_playlist_id="spotify_playlist_id_2"
        )

    def test_playlist_pair_playlists(self):
        """Playlists that return the spotify \
            and apple IDs are correctly identified"""

        first_playlist_pair = PlaylistPairs.objects.get(pk=1)
        second_playlist_pair = PlaylistPairs.objects.get(pk=2)
        self.assertEqual(
            first_playlist_pair.get_apple_playlist_id(),
            'apple_playlist_id_1'
        )
        self.assertEqual(
            first_playlist_pair.get_spotify_playlist_id(),
            'spotify_playlist_id_1'
        )
        self.assertEqual(
            first_playlist_pair.__str__(),
            "apple-apple_playlist_id_1_spotify-spotify_playlist_id_1"
            )
        self.assertEqual(
            second_playlist_pair.get_apple_playlist_id(),
            'apple_playlist_id_2'
        )
        self.assertEqual(
            second_playlist_pair.get_spotify_playlist_id(),
            'spotify_playlist_id_2'
        )
        self.assertEqual(
            second_playlist_pair.__str__(),
            "apple-apple_playlist_id_2_spotify-spotify_playlist_id_2"
        )
