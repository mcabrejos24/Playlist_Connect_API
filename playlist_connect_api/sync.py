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
    spotify_refresh_token = 'https://accounts.spotify.com/api/token'
    spotify_check_auth = 'https://api.spotify.com/v1/me'

    def get_apple_isrc(song_ids, header):
        isrc = set()
        for id in song_ids:
            response_json = StartSync.api_get('apple isrc', StartSync.apple_to_isrc_url+id, header)
            if response_json and response_json['data'] and response_json['data'][0] and response_json['data'][0]['attributes'] and response_json['data'][0]['attributes']['isrc']:
                isrc.add(response_json['data'][0]['attributes']['isrc'])
        return isrc

    @staticmethod
    def get_playlist_songs(service, url, header, playlist_id):
        response_json = StartSync.api_get(service, url+playlist_id+'/tracks', header=header)
        if not response_json:
            return 0

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
        response = requests.post(url, data=payload, headers=header, timeout=10)
        if not response:
            print(f'Failed in making {service} POST call, url: {url}')
            return
        return response

    @staticmethod
    def api_get(service, url, header):
        try: 
            response = requests.get(url, headers=header, timeout=10)
            # return response content
            if response and response.status_code and response.content:
                if response.status_code != '200':
                    print(f'400 level response from {service} GET, url: {url}, code: {response.status_code}')
                return response
        except requests.Timeout:
            print(f'Request timed out, failed get a response, {service} GET, url: {url}')
            return -1
        except requests.ConnectionError:
            print(f'Connection error, failed get a response, {service} GET, url: {url}')
            return -1

    @staticmethod
    def add_playlist_songs_to(service, url_isrc, isrcs, header, url_playlist, playlist_id):
        if not isrcs:
            return
        song_codes = []

        for isrc in isrcs:
            url = url_isrc + isrc
            response_json = StartSync.api_get(service+'from isrc to id', url, header)
            if response_json.status != 200:
                return 0
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

    @staticmethod # need to return print message and return based on error, expired or bad request
    def checkSpotifyAuth(header):
        response  = StartSync.api_get('spotify check auth', StartSync.spotify_check_auth, header)
        if response  == -1:
            print('checkSpotifyAuth: failed to get api response')
            return -1
        if response.status_code == 200:
            return True
        response_json = json.loads(response.content)
        print(response_json)
        if response.status_code == '400' and response_json['error_description'] and response_json['error_description'] == 'Refresh token revoked':
            return False
        print('Api error: ' + response.status_code + ' \nResponse content: \n' + response_json)
        return -1

    @staticmethod
    def refreshSpotifyAuth(playlistPair):
        refresh_code = base64.b64decode(f'{playlistPair.spotify_refresh_1}{playlistPair.spotify_refresh_2}').decode('ascii')
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': f'{refresh_code}',
            'client_id': config("SPOTIFY_CLIENT_ID")
        }
        response_json = StartSync.api_post('spotify refresh auth token', StartSync.spotify_refresh_token, header, payload)

        if not response_json:
            print('Error in getting the Spotify refresh auth token')
            return False;
        
        access_token = response_json['access_token']
        refresh_token = response_json['refresh_token']

        # encodes the access token
        access_token_bytes = access_token.encode('ascii')
        access_token_bytes_encoded = base64.b64encode(access_token_bytes)
        access_token_encoded = access_token_bytes_encoded.decode('ascii')
        access_token_encoded_array = [access_token_encoded[0:128], access_token_encoded[128:256], access_token_encoded[256:len(access_token_encoded)]]

        #encodes the refresh token
        access_token_bytes = refresh_token.encode('ascii')
        access_token_bytes_encoded = base64.b64encode(access_token_bytes)
        refresh_token_encoded = access_token_bytes_encoded.decode('ascii')
        refresh_token_encoded_array = [refresh_token_encoded[0:128], refresh_token_encoded[128:len(refresh_token_encoded)]]

        playlistPair.spotify_token_1 = access_token_encoded_array[0]
        playlistPair.spotify_token_2 = access_token_encoded_array[1]
        playlistPair.spotify_token_3 = access_token_encoded_array[2]
        playlistPair.spotify_refresh_1 = refresh_token_encoded_array[0]
        playlistPair.spotify_refresh_2 = refresh_token_encoded_array[1]
        playlistPair.save()
        
        return {
            'Authorization': f'Bearer {access_token}',
        }


    @staticmethod
    def sync(playlistPairObject):
        spotify_auth = base64.b64decode(f'{playlistPairObject.spotify_token_1}{playlistPairObject.spotify_token_2}{playlistPairObject.spotify_token_3}').decode('ascii')
        apple_auth = base64.b64decode(f'{playlistPairObject.apple_token_1}{playlistPairObject.apple_token_2}{playlistPairObject.apple_token_3}').decode('ascii')
        spotify_header = {
            'Authorization': f'Bearer {spotify_auth}',
        }
        apple_header = {
            'Authorization': f'Bearer {config("APPLE_DEVELOPER_TOKEN")}',
            'music-user-token': apple_auth
        }

        spotifyAuthIsValid = StartSync.checkSpotifyAuth(spotify_header)
        if spotifyAuthIsValid == -1:
            return [0, 0]
        if not spotifyAuthIsValid:
            refreshSuccessful = StartSync.refreshSpotifyAuth(playlistPairObject)
            if not refreshSuccessful:
                return [0, 0]
            spotify_header = refreshSuccessful

        spotify_songs = StartSync.get_playlist_songs('spotify', StartSync.spotify_url, spotify_header, playlistPairObject.spotify_playlist_id)
        apple_songs = StartSync.get_playlist_songs('apple', StartSync.apple_url, apple_header, playlistPairObject.apple_playlist_id)

        if spotify_songs == 0 or apple_songs == 0:
            print('Failed to get playlist songs from spotify or apple. Additional details will be in above logs.')
            return [spotify_songs, apple_songs]

        spotify_successful = StartSync.add_playlist_songs_to('spotify', StartSync.spotify_from_isrc, apple_songs-spotify_songs, spotify_header, StartSync.spotify_url, playlistPairObject.spotify_playlist_id)
        apple_successful = StartSync.add_playlist_songs_to('apple', StartSync.apple_from_isrc, spotify_songs-apple_songs, apple_header, StartSync.apple_url, playlistPairObject.apple_playlist_id)

        return [apple_successful, spotify_successful]
