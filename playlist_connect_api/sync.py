from operator import truediv
import requests
import base64
import json
from decouple import config

class StartSync():
    """Does the initial sync for the playlists"""
    spotify_url = 'https://api.spotify.com/v1/playlists/'
    apple_url = 'https://api.music.apple.com/v1/me/library/playlists/'
    apple_to_isrc_url = 'https://api.music.apple.com/v1/catalog/us/songs/'
    spotify_from_isrc = 'https://api.spotify.com/v1/search?type=track&q=isrc:'
    apple_from_isrc = 'https://api.music.apple.com/v1/catalog/us/songs?filter[isrc]='

    def get_apple_isrc(song_ids, header):
        isrc = set()
        for id in song_ids:
            response_json = StartSync.api_get('apple isrc', StartSync.apple_to_isrc_url+id, header)
            isrc.add(response_json['data'][0]['attributes']['isrc'])
        return isrc

    @staticmethod
    def get_playlist_songs(service, url, header, playlist_id):
        response_json = StartSync.api_get(service, url+playlist_id+'/tracks', header=header)
        songs_isrc = set()

        # spotify returns songs with a attribute of isrc
        if service == 'spotify': 
            for song in response_json['items']:
                if song['track'] and song['track']['external_ids'] and song['track']['external_ids']['isrc']:
                    songs_isrc.add(song['track']['external_ids']['isrc'])
        # apple music returns songs with an id that then need to be used to find the isrc in another call, hence function get_apple_isrc() is used
        elif service == 'apple':
            apple_song_ids = set()
            for song in response_json['data']:
                if song['attributes'] and song['attributes']['playParams'] and song['attributes']['playParams']['catalogId']:
                    apple_song_ids.add(song['attributes']['playParams']['catalogId'])
                songs_isrc = StartSync.get_apple_isrc(apple_song_ids, header)

        return songs_isrc

    @staticmethod
    def api_post(service, url, header, payload):
        response = requests.post(url, data=payload, headers=header)
        if not response:
            print(f'Failed in making {service} POST call, url: {url}')
            return
        return response

    @staticmethod
    def api_get(service, url, header):
        response = requests.get(url, headers=header);
        if not response:
            print(f'Failed in making {service} GET call, url: {url}')
            return
        return json.loads(response.content)

    @staticmethod
    def add_playlist_songs_to(service, url_isrc, isrcs, header, url_playlist, playlist_id):
        if not isrcs:
            return
        song_codes = []

        for isrc in isrcs:
            url = url_isrc + isrc
            response_json = StartSync.api_get(service+'from isrc to id', url, header)
            if service == 'spotify':
                if response_json and response_json['tracks'] and response_json['tracks']['items'] and response_json['tracks']['items'][0] and response_json['tracks']['items'][0]['uri']:
                    song_codes.append(response_json['tracks']['items'][0]['uri'])
            elif service == 'apple':
                if response_json and response_json['data'] and response_json['data'][0] and response_json['data'][0]['id']:
                    song_codes.append({"id": f"{response_json['data'][0]['id']}", "type": "songs"})
        if not song_codes:
            return
        
        url = url_playlist + playlist_id + '/tracks'

        if service == 'spotify':
            payload = f'{{"uris": {song_codes}}}'
        elif service == 'apple':
            payload = f'{{"data": {song_codes}}}'
        
        if not payload:
            return
        payload = payload.replace("'", '"')
        res = StartSync.api_post(service, url, header, payload)

        return res

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

        spotify_successful = StartSync.add_playlist_songs_to('spotify', StartSync.spotify_from_isrc, apple_songs-spotify_songs, spotify_header, StartSync.spotify_url, playlistPairObject.spotify_playlist_id)
        apple_successful = StartSync.add_playlist_songs_to('apple', StartSync.apple_from_isrc, spotify_songs-apple_songs, apple_header, StartSync.apple_url, playlistPairObject.apple_playlist_id)

        return [apple_successful, spotify_successful]