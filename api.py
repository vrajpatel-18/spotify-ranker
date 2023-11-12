import requests
import json
from difflib import SequenceMatcher
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


def getArtists(search):
    searchLimit = '20'
    searchType = "artist"
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
    formatted_json = json.dumps(json_data)
    return formatted_json
    
    
    
def getAlbums(search):
    searchLimit = '20'
    searchType = "album"
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
    formatted_json = json.dumps(json_data)
    return formatted_json