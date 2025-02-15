import requests
import json
import time
import hashlib
import base64
import os
from flask import session
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
client_id_key = os.environ.get("CLIENT_ID")
client_secret_key = os.environ.get("CLIENT_SECRET")

def create_client_credentials_token():
    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id_key,
            "client_secret": client_secret_key
        }
    )

    if auth_response.status_code == 200:
        token_info = auth_response.json()
        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        return token_info
    else:
        print(f"Failed to obtain client credentials token: {auth_response.status_code}")
        return None


def token():
    # Get the logged-in user's token from the session
    user_id = session.get('user_id', None)
    user_token_info = session.get(f'{user_id}_token', None)  # Use {user_id}_token
    print(user_token_info)

    if user_token_info:
        # Return the logged-in user's token
        return user_token_info
    
    # If the user is not logged in, use a default access token
    default_token_info = session.get('default_token_info', None)
    
    if not default_token_info:
        # Generate a new default token if not found in the session
        default_token_info = create_client_credentials_token()
        session['default_token_info'] = default_token_info
    
    return default_token_info


def getSongPopularity(songID):
    access_token = token()['access_token']
    url = 'https://api.spotify.com/v1/tracks/' + songID
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    song_response = requests.get(url, headers=headers)
    song_data = song_response.json()
    return song_data['popularity']

def generateID(input_string):
    hash_object = hashlib.sha256(input_string.encode())
    hash_digest = hash_object.digest()
    base64_encoded = base64.b64encode(hash_digest)
    id_str = base64_encoded.decode("utf-8").replace("/", "").replace("+", "")
    return id_str[:22]

def durationGapDays(date1, date2):
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    return (d2 - d1).days



def getArtists(search):
    access_token = token()['access_token']
    search = search.replace("#", "")
    print("Get Artists", search)
    searchLimit = '50'
    searchType = 'artist'
    url = 'https://api.spotify.com/v1/search?q=' + search + '&type=' + searchType + '&limit=' + searchLimit
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    artist_response = requests.get(url, headers=headers)
    artist_data = artist_response.json()

    artists = []
    data = {}
    if artist_data['artists']['total'] == 0:
        return json.dumps(data, indent=4)
    for artist in artist_data['artists']['items']:
        images = artist['images']
        if (len(images) > 0) and len(artists) < 25:
            curr_artist = {}
            curr_artist['name'] = artist['name']
            curr_artist['id'] = artist['id']
            curr_artist['followers'] = artist['followers']['total']
            curr_artist['img'] = artist['images'][0]['url']
            artists.append(curr_artist)
    
    data['artists'] = artists
        
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json
    
    
    
def getAlbums(search):
    access_token = token()['access_token']
    search = search.replace("#", "")
    print("Get Albums", search)
    searchLimit = '50'
    searchType = 'album'
    url = 'https://api.spotify.com/v1/search?q=' + search + '&type=' + searchType + '&limit=' + searchLimit
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    album_response = requests.get(url, headers=headers)
    album_data = album_response.json()

    albums = []
    data = {}
    if album_data['albums']['total'] == 0:
        return json.dumps(data, indent=4)
    for album in album_data['albums']['items']:
        images = album['images']
        if (len(images) > 0) and len(albums) < 25:
            curr_album = {}
            curr_album['name'] = album['name']
            curr_album['id'] = album['id']
            artists = []
            for artist in album['artists']:
                artists.append(artist['name'])
            curr_album['artists'] = artists
            curr_album['img'] = album['images'][0]['url']
            curr_album['year'] = album['release_date'][0:4]
            append = True
            for existing_album in albums:
                if existing_album['name'] == curr_album['name'] and existing_album['artists'][0] == curr_album['artists'][0]:
                    append = False
            if append:
                albums.append(curr_album)
    
    data['albums'] = albums
        
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json


def getPlaylists(search):
    access_token = token()['access_token']
    print("Get Playlists", search)
    searchLimit = '10'
    searchType = 'playlist'
    url = 'https://api.spotify.com/v1/search?q=' + search + '&type=' + searchType + '&limit=' + searchLimit
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    playlist_response = requests.get(url, headers=headers)
    playlist_data = playlist_response.json()

    playlists = []
    data = {}
    for playlist in playlist_data['playlists']['items']:
        images = playlist['images']
        if (len(images) > 0) and len(playlists) < 10:
            curr_playlist = {}
            curr_playlist['name'] = playlist['name']
            curr_playlist['id'] = playlist['id']
            curr_playlist['img'] = playlist['images'][0]['url']
            curr_playlist['owner'] = playlist['owner']['display_name']
            playlists.append(curr_playlist)

    data['playlists'] = playlists

    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json



def getAlbumSongs(albumID):
    access_token = token()['access_token']
    print("Get Album Songs", albumID)
    url = 'https://api.spotify.com/v1/albums/' + albumID
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    album_response = requests.get(url, headers=headers)
    album_data = album_response.json()
    
    songs = []
    data = {}
    for song in album_data['tracks']['items']:
        curr_song = {}
        curr_song['name'] = song['name']
        curr_song['id'] = song['id']
        artists = []
        for artist in song['artists']:
            artists.append(artist['name'])
        curr_song['artists'] = artists
        curr_song['img'] = album_data['images'][0]['url']
        curr_song['date'] = album_data['release_date']
        curr_song['album'] = album_data['name']
        songs.append(curr_song)
    
    data['songs'] = songs
    
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json



def getPlaylistSongs(playlistID, offset):
    access_token = token()['access_token']
    print("Get Playlist Songs", playlistID, access_token)
    url = 'https://api.spotify.com/v1/playlists/' + playlistID + '/tracks?limit=100&offset=' + str(offset)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    playlist_response = requests.get(url, headers=headers)
    playlist_data = playlist_response.json()
    
    songs = []
    data = {}
    if 'items' not in playlist_data:
        data['songs'] = songs
        json_data = data
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json
    for song in playlist_data['items']:
        curr_song = {}
        curr_song['name'] = song['track']['name']
        curr_song['id'] = song['track']['id']
        curr_song['date'] = song['track']['album']['release_date']
        curr_song['album'] = song['track']['album']['name']
        artists = []
        for artist in song['track']['artists']:
            artists.append(artist['name'])
        curr_song['artists'] = artists
        if song['is_local']:
            curr_song['img'] = 'https://player.listenlive.co/templates/StandardPlayerV4/webroot/img/default-cover-art.png'
            curr_song['id'] = generateID(song['track']['name'] + song['track']['album']['name'] + artists[0])
            print('hi')
            curr_song['type'] = 'local'
        else:
            curr_song['img'] = song['track']['album']['images'][0]['url']
            curr_song['type'] = 'spotify'
        songs.append(curr_song)
    
    data['songs'] = songs
    
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json


def getAllPlaylistSongs(playlistID):
    print("Get All Playlist Songs", playlistID)
    offset = 0
    songs = []
    while True:
        playlist_data = json.loads(getPlaylistSongs(playlistID, offset))
        if len(playlist_data['songs']) == 0:
            break
        for song in playlist_data['songs']:
            songs.append(song)
        offset += 100
    
    data = {}
    data['songs'] = songs
    
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json



def getArtistAlbums(artistID):
    access_token = token()['access_token']
    print("Get Artist Albums", artistID)
    url = 'https://api.spotify.com/v1/artists/' + artistID + '/albums?include_groups=album'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    artist_response = requests.get(url, headers=headers)
    artist_data = artist_response.json()
    
    albums = []
    data = {}
    for album in artist_data['items']:
        curr_album = {}
        curr_album['name'] = album['name']
        curr_album['id'] = album['id']
        artists = []
        for artist in album['artists']:
            artists.append(artist['name'])
        curr_album['artists'] = artists
        curr_album['img'] = album['images'][0]['url']
        curr_album['year'] = album['release_date'][0:4]
        albums.append(curr_album)
    
    if albums:
        albums.reverse()
    data['albums'] = albums
        
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json


def getArtistSingles(artistID):
    access_token = token()['access_token']
    print("Get Artist Singles", artistID)
    url = 'https://api.spotify.com/v1/artists/' + artistID + '/albums?include_groups=single&offset=0&limit=50&locale=en-US,en;q=0.9'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    artist_response = requests.get(url, headers=headers)
    artist_data = artist_response.json()
    
    singles = []
    data = {}
    for single in artist_data['items']:
        if single['artists'][0]['id'] == artistID:
            curr_single = {}
            curr_single['name'] = single['name']
            curr_single['id'] = single['id']
            artists = []
            for artist in single['artists']:
                artists.append(artist['name'])
            curr_single['artists'] = artists
            curr_single['img'] = single['images'][0]['url']
            curr_single['year'] = single['release_date'][0:4]
            singles.append(curr_single)
    
    if singles:
        singles.reverse()
    data['albums'] = singles
        
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json



def getArtistSongs(artistID):
    print("Get Artist Songs", artistID)
    albums_data = json.loads(getArtistAlbums(artistID))
    singles_data = json.loads(getArtistSingles(artistID))
    
    songs = []
    data = {}
    for album in albums_data['albums']:
        album_data = json.loads(getAlbumSongs(album['id']))
        for song in album_data['songs']:
            append = True
            for existing_song in songs:
                if existing_song['name'] == song['name'] and existing_song['artists'] == song['artists'] and durationGapDays(existing_song['date'], song['date']) < 365:
                    append = False
            if append:
                songs.append(song)
    for single in singles_data['albums']:
        single_data = json.loads(getAlbumSongs(single['id']))
        for song in single_data['songs']:
            valid = True
            new_songs = []
            for curr_song in songs:
                if song['name'] in curr_song['name'] or curr_song['name'] in song['name'] and song['artists'] == curr_song['artists']:
                    songPop = getSongPopularity(song['id'])
                    currSongPop = getSongPopularity(curr_song['id'])
                    if currSongPop > songPop:
                        valid = False
                        new_songs.append(curr_song)
                else:
                    new_songs.append(curr_song)
            songs = new_songs
            if valid:
                songs.append(song)
    
    data['songs'] = songs
    
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json
    
    


def getAlbumName(albumId):
    access_token = token()['access_token']
    url = 'https://api.spotify.com/v1/albums/' + albumId
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    album_response = requests.get(url, headers=headers)
    album_data = album_response.json()
    if len(album_data) == 1:
        return ''
    else:
        return album_data['name']
    
    
def getArtistName(artistId):
    access_token = token()['access_token']
    url = 'https://api.spotify.com/v1/artists/' + artistId
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    artist_response = requests.get(url, headers=headers)
    artist_data = artist_response.json()
    if len(artist_data) == 1:
        return ''
    else:
        return artist_data['name']
    
def getPlaylistName(playlistId):
    access_token = token()['access_token']
    print(playlistId)
    url = 'https://api.spotify.com/v1/playlists/' + playlistId
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    playlist_response = requests.get(url, headers=headers)
    playlist_data = playlist_response.json()
    if len(playlist_data) == 1:
        return ''
    else:
        return playlist_data['name']