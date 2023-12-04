import requests
import json
import time
import os
from dotenv import load_dotenv


load_dotenv()
client_id_key = os.environ.get("CLIENT_ID")
client_secret_key = os.environ.get("CLIENT_SECRET")


# CHECK IF NEW TOKEN NEEDS TO BE GENERATED
token_expired = False
access_token = ''
with open('token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
    if token_data['expire_time'] < time.time():
        token_expired = True
    access_token = token_data['access_token']
    
if token_expired:
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id_key,
        "client_secret": client_secret_key
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        token_data['expire_time'] = time.time() + token_data['expires_in']
        access_token = token_data['access_token']
        with open('token.json', 'w', encoding='utf-8') as f:
            json.dump(token_data, f, ensure_ascii=False, indent=4)
    else:
        print(f"Token request failed with status code {response.status_code}")







def getSongPopularity(songID):
    url = 'https://api.spotify.com/v1/tracks/' + songID
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    song_response = requests.get(url, headers=headers)
    song_data = song_response.json()
    return song_data['popularity']



def getArtists(search):
    print("Get Artists", search)
    searchLimit = '20'
    searchType = 'artist'
    url = 'https://api.spotify.com/v1/search?q=' + search + '&type=' + searchType + '&limit=' + searchLimit
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    artist_response = requests.get(url, headers=headers)
    artist_data = artist_response.json()

    artists = []
    data = {}
    for artist in artist_data['artists']['items']:
        images = artist['images']
        if (len(images) > 0) and len(artists) < 10:
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
    print("Get Albums", search)
    searchLimit = '20'
    searchType = 'album'
    url = 'https://api.spotify.com/v1/search?q=' + search + '&type=' + searchType + '&limit=' + searchLimit
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    album_response = requests.get(url, headers=headers)
    album_data = album_response.json()

    albums = []
    data = {}
    for album in album_data['albums']['items']:
        images = album['images']
        if (len(images) > 0) and len(albums) < 10:
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
    
    data['albums'] = albums
        
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json


def getPlaylists(search):
    print("Get Playlists", search)
    searchLimit = '20'
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



def findLocalSongInfo(songName, albumName):
    data = {}
    print("Find Local Song Info", songName, albumName)
    
    url = 'https://api.spotify.com/v1/search?q=' + albumName + '&type=album&limit=10'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    album_response = requests.get(url, headers=headers)
    album_data = album_response.json()
    
    if len(album_data['albums']['items']) == 0:
        return None
    else:
        for album in album_data['albums']['items']:
            str1 = album['name'].lower()
            str2 = albumName.lower()
            if str1 in str2 or str2 in str1:
                rawAlbumData = getAlbumSongs(album['id'])
                albumData = json.loads(rawAlbumData)
                for song in albumData['songs']:
                    str1 = song['name'].lower()
                    str2 = songName.lower()
                    if str1 in str2 or str2 in str1:
                        data['img'] = song['img']
                        data['date'] = song['date']
                        data['id'] = song['id']
                        data['artists'] = song['artists']
                        data['album'] = album['name']
                        json_data = data
                        formatted_json = json.dumps(json_data, indent=4)
                        return formatted_json
    return None


def getPlaylistSongs(playlistID, offset):
    print("Get Playlist Songs", playlistID)
    url = 'https://api.spotify.com/v1/playlists/' + playlistID + '/tracks?limit=100&offset=' + str(offset)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    playlist_response = requests.get(url, headers=headers)
    playlist_data = playlist_response.json()
    
    songs = []
    data = {}
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
            # local_data = findLocalSongInfo(song['track']['name'], song['track']['album']['name'])
            # if local_data:
            #     loaded_data = json.loads(local_data)
            #     curr_song['img'] = loaded_data['img']
            #     curr_song['id'] = loaded_data['id']
            #     curr_song['date'] = loaded_data['date']
            #     curr_song['album'] = loaded_data['album']
            #     curr_song['artists'] = loaded_data['artists']
            # else:
            #     curr_song['img'] = 'https://player.listenlive.co/templates/StandardPlayerV4/webroot/img/default-cover-art.png'
            curr_song['img'] = 'https://player.listenlive.co/templates/StandardPlayerV4/webroot/img/default-cover-art.png'
        else:
            curr_song['img'] = song['track']['album']['images'][0]['url']
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


# print(getAllPlaylistSongs('6YSPNOhpq3T3NlxrsSNnMd'))



def getArtistAlbums(artistID):
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
    
    data['albums'] = albums
        
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json


def getArtistSingles(artistID):
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
    
    

