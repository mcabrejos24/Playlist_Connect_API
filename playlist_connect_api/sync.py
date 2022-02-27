from operator import truediv
import requests
import base64
import json
from decouple import config

class StartSync():
    """Does the initial sync for the playlists"""
    # spotify_playlist_url = f'https://api.music.apple.com/v1/me/library/playlists'
    spotify_url = 'https://api.spotify.com/v1/playlists/'
    apple_url = 'https://api.music.apple.com/v1/me/library/playlists/'

    def get_apple_isrc(song_ids, header):
        url = 'https://api.music.apple.com/v1/catalog/us/songs/'
        isrc = set()
        for id in song_ids:
            response = requests.get(url+id, headers=header);
            if not response:
                print('Failed to get ISRC')
                return
            response_json = json.loads(response.content)
            isrc.add(response_json['data'][0]['attributes']['isrc'])


        return isrc

    @staticmethod
    def get_playlist_songs(service, url, header, playlist_id):
        response_json = StartSync.api_get(service, url+playlist_id+'/tracks', header=header)

        songs_isrc = set()
        if service == 'spotify':
            for song in response_json['items']:
                if song['track'] and song['track']['external_ids'] and song['track']['external_ids']['isrc']:
                    songs_isrc.add(song['track']['external_ids']['isrc'])
            return songs_isrc
        elif service == 'apple':
            apple_song_ids = set()
            for song in response_json['data']:
                if song['attributes'] and song['attributes']['playParams'] and song['attributes']['playParams']['catalogId']:
                    apple_song_ids.add(song['attributes']['playParams']['catalogId'])
                songs_isrc = StartSync.get_apple_isrc(apple_song_ids, header)
            return songs_isrc
        return ['FAILED TO GET ANY SONG ISRC CODES']

    @staticmethod
    def api_get(service, url, header):
        res = requests.get(url, headers=header);
        if not res:
            print(f'Failed in making {service} GET call, url: {url}')
            return
        return json.loads(res.content)

    @staticmethod
    def api_post(service, url, header, payload):
        result = requests.post(url, data=payload, headers=header)
        return result

    @staticmethod
    def add_playlist_songs_to(service, isrcs, header, playlist_id):
        if not isrcs:
            return
        if service == 'apple':
            song_ids = []
            for isrc in isrcs:
                url = f'https://api.music.apple.com/v1/catalog/us/songs?filter[isrc]={isrc}'
                response_json = StartSync.api_get(service, url, header)
                if not response_json:
                    print(f'Failed in making getting songs, url: {url}')
                    return
                if response_json['data'] and response_json['data'][0] and response_json['data'][0]['id']:
                    song_ids.append({"id": f"{response_json['data'][0]['id']}", "type": "songs"})
            
            url = f'https://api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks'
            payload = f'{{"data": {song_ids}}}'
            payload = payload.replace("'", '"')
            res = StartSync.api_post(service, url, header, payload)
            return res
        elif service == 'spotify':
            uris = []
            for isrc in isrcs:
                url = f'https://api.spotify.com/v1/search?type=track&q=isrc:{isrc}'
                response_json = StartSync.api_get(service, url, header)

                if not response_json:
                    print(f'Failed in making getting uris, url: {url}')
                    return
                if response_json['tracks'] and response_json['tracks']['items'] and response_json['tracks']['items'][0] and response_json['tracks']['items'][0]['uri']:
                    uris.append(response_json['tracks']['items'][0]['uri'])

            url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
            payload = f'{{"uris": {uris}}}'
            payload = payload.replace("'", '"')
            res = StartSync.api_post(service, url, header, payload)
            return res
        return

    @staticmethod
    def sync(playlistPairObject):
        spotify_auth = str(base64.b64decode(f'{playlistPairObject.spotify_token_1}{playlistPairObject.spotify_token_2}{playlistPairObject.spotify_token_3}'), "utf-8")
        apple_auth = str(base64.b64decode(f'{playlistPairObject.apple_token_1}{playlistPairObject.apple_token_2}{playlistPairObject.apple_token_3}'), "utf-8")
        spotify_header = {
            'Authorization': f'Bearer {spotify_auth}',
        }
        apple_header = {
            'Authorization': f'Bearer {config("APPLE_DEVELOPER_TOKEN")}',
            'music-user-token': apple_auth
        }


        spotify_songs = StartSync.get_playlist_songs('spotify', StartSync.spotify_url, spotify_header, playlistPairObject.spotify_playlist_id)
        apple_songs = StartSync.get_playlist_songs('apple', StartSync.apple_url, apple_header, playlistPairObject.apple_playlist_id)

        print(spotify_auth)
        print(' ')
        print(apple_auth)

        spotify_successful = StartSync.add_playlist_songs_to('spotify', apple_songs-spotify_songs, spotify_header, playlistPairObject.spotify_playlist_id)
        apple_successful = StartSync.add_playlist_songs_to('apple', spotify_songs-apple_songs, apple_header, playlistPairObject.apple_playlist_id)


        print(spotify_successful)
        print(apple_successful)
        return apple_successful and spotify_successful