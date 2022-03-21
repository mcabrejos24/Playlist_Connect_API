from django.test import TestCase
from playlist_connect_api.models import PlaylistPairs
from playlist_connect_api.sync import StartSync


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
            "apple_playlist_id_1"
        )
        self.assertEqual(
            first_playlist_pair.get_spotify_playlist_id(),
            "spotify_playlist_id_1"
        )
        self.assertEqual(
            first_playlist_pair.__str__(),
            "apple-apple_playlist_id_1_spotify-spotify_playlist_id_1"
        )
        self.assertEqual(
            second_playlist_pair.get_apple_playlist_id(),
            "apple_playlist_id_2"
        )
        self.assertEqual(
            second_playlist_pair.get_spotify_playlist_id(),
            "spotify_playlist_id_2"
        )
        self.assertEqual(
            second_playlist_pair.__str__(),
            "apple-apple_playlist_id_2_spotify-spotify_playlist_id_2"
        )


class StartSyncTestCase(TestCase):
    def test_sync_no_object(self):
        """Tests function with no object passed"""
        self.assertEqual(
            StartSync.sync(""),
            [0, 0]
        )

    def test_sync_no_params(self):
        """Tests function with no params in object"""
        mockPlaylistPair = type('', (), {
            "apple_token_1": "",
            "apple_token_2": "",
            "apple_token_3": "",
            "spotify_token_1": "",
            "spotify_token_2": "",
            "spotify_token_3": "",
            "spotify_refresh_1": "",
            "spotify_refresh_2": "",
            "apple_playlist_id": "",
            "spotify_playlist_id": ""
        })()

        self.assertEqual(
            StartSync.sync(mockPlaylistPair),
            [0, 0]
        )

    def test_sync_half_params(self):
        """Tests function with half params in object"""
        mockPlaylistPair = type('', (), {
            "apple_token_1": "test",
            "apple_token_2": "test",
            "apple_token_3": "test",
            "spotify_token_1": "test",
            "spotify_token_2": "test",
            "spotify_token_3": "",
            "spotify_refresh_1": "",
            "spotify_refresh_2": "",
            "apple_playlist_id": "",
            "spotify_playlist_id": ""
        })()

        self.assertEqual(
            StartSync.sync(mockPlaylistPair),
            [0, 0]
        )

    def test_api_get(self):
        """Tests api GET function"""
        mockHeader = {
            "Authorization": "",
        }
        self.assertEqual(
            StartSync.api_get(
                'spotify',
                'http://example.com',
                mockHeader
            ).status_code,
            200
        )

    def test_api_post(self):
        """Tests api POST function"""
        mockHeader = {
            "Authorization": "",
        }
        mockPayload = {
            "mock1": "",
            "mock2": "",
            "mock3": "",
        }
        self.assertEqual(
            StartSync.api_post(
                'spotify',
                'http://example.com',
                mockHeader,
                mockPayload
            ).status_code,
            200
        )
