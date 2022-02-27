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
        isrc = []
        for id in song_ids:
            response = requests.get(url+id, headers=header);
            if not response:
                print('Failed to get ISRC')
                return
            response_json = json.loads(response.content.decode('utf8').replace("'", '"'))
            isrc.append(response_json['data'][0]['attributes']['isrc'])


        return isrc

    @staticmethod
    def get_playlist_songs(service, url, header, playlist_id):
        response = requests.get(url+playlist_id+'/tracks', headers=header);
        
        if not response:
            print('Failed to get your songs!!!')
            return
        response_json = json.loads(response.content.decode('utf8').replace("'", '"'))

        songs_isrc = []
        if service == 'spotify':
            for song in response_json['items']:
                if song['track'] and song['track']['external_ids'] and song['track']['external_ids']['isrc']:
                    songs_isrc.append(song['track']['external_ids']['isrc'])
            return songs_isrc
        elif service == 'apple':
            apple_song_ids = []
            for song in response_json['data']:
                if song['attributes'] and song['attributes']['playParams'] and song['attributes']['playParams']['catalogId']:
                    apple_song_ids.append(song['attributes']['playParams']['catalogId'])
                songs_isrc = StartSync.get_apple_isrc(apple_song_ids, header)
            return songs_isrc
        return ['FAILED TO GET ANY SONG ISRC CODES']

        # then make sure they overlapping songs are not synced
        # and then add them
        # what we can do is either get the intersection and remove them from both
        # or add all songs either way and check if both apple music and spotify allow us to add it
        # if duplicates then maybe oh well, but lets try it
        # will grab songs by either a specific song code
        # or by finding, artist, song name, and album

    @staticmethod
    def sync(playlistPairObject):

        spotify_auth = str(base64.b64decode(f'{playlistPairObject.spotify_token_1}{playlistPairObject.spotify_token_2}{playlistPairObject.spotify_token_3}'), "utf-8")
        spotify_header = {
            'Authorization': f'Bearer {spotify_auth}',
        }
        spotify_songs = StartSync.get_playlist_songs('spotify', StartSync.spotify_url, spotify_header, playlistPairObject.spotify_playlist_id)
        

        apple_auth = str(base64.b64decode(f'{playlistPairObject.apple_token_1}{playlistPairObject.apple_token_2}{playlistPairObject.apple_token_3}'), "utf-8")
        apple_header = {
            'Authorization': f'Bearer {config("APPLE_DEVELOPER_TOKEN")}',
            'music-user-token': apple_auth
        }
        apple_songs = StartSync.get_playlist_songs('apple', StartSync.apple_url, apple_header, playlistPairObject.apple_playlist_id)

        # add both lists to one set, to erase overlappings, then add to each and just don't add what's already there

        # make both sets, then from one remove overlappings, then add 

        # get intersection (O(smallest list))
        # remove intersection from list 1 and then remaining send to opp service (O(intersection )) + O(length of remaining list)
        # do same for list 2 (O(intersection )) + O(length of remaining list)

        # loop through songs to add and check if other list contains (O(list))
        # same for other

        # 12345  23456

        # 5 1 1
        # 5 5

        print(spotify_songs)
        print(apple_songs)

        return;