from flask import Flask, render_template, request, jsonify, url_for, session, redirect
import api
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import os
from dotenv import load_dotenv


load_dotenv()
client_id_key = os.environ.get("CLIENT_ID")
client_secret_key = os.environ.get("CLIENT_SECRET")

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = os.environ.get("APP_SECRET_KEY")
TOKEN_INFO = 'token_info'

@app.route('/')
def index():
    return render_template('index.html', **locals())

@app.route('/ranker')
def ranker():
    return render_template('ranker.html', **locals())

@app.route('/login')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    # update token in token.json
    with open('token.json', 'w') as file:
        json.dump(token_info, file, indent=4)
    return redirect(url_for('index',_external=True))


@app.route('/artist', methods=['POST'])
def getArtists():
    if request.method == 'POST':
        search = request.form['search']
        result = api.getArtists(search)
        return jsonify(result)
    
@app.route('/album', methods=['POST'])
def getAlbums():
    if request.method == 'POST':
        search = request.form['search']
        result = api.getAlbums(search)
        return jsonify(result)
    
# @app.route('/playlist', methods=['POST'])
# def getPlaylists():
#     if request.method == 'POST':
#         search = request.form['search']
#         result = api.getPlaylists()
#         return jsonify(result)
@app.route('/playlist', methods=['POST'])
def getPlaylists():
    if request.method == 'POST':
        search = request.form['search']
        try:
            token_info = get_token()
        except:
            print("User not logged in")
            if search == '':
                data = {}
                return jsonify(data)
            else:
                result = api.getPlaylists(search)
                return jsonify(result)
        def getUserPlaylists(offset):
            print("Get User Playlists, Offset=", offset)
            sp = spotipy.Spotify(auth=token_info['access_token'])
            playlist_data = sp.current_user_playlists(50, offset)
            playlists = []
            data = {}
            if playlist_data['total'] == 0:
                return json.dumps(data, indent=4)
            for playlist in playlist_data['items']:
                curr_playlist = {}
                curr_playlist['name'] = playlist['name']
                curr_playlist['id'] = playlist['id']
                if len(playlist['images']) > 0:
                    curr_playlist['img'] = playlist['images'][0]['url']
                else:
                    curr_playlist['img'] = 'https://player.listenlive.co/templates/StandardPlayerV4/webroot/img/default-cover-art.png'
                curr_playlist['owner'] = playlist['owner']['display_name']
                playlists.append(curr_playlist)
            
            data['playlists'] = playlists
            
            json_data = data
            formatted_json = json.dumps(json_data, indent=4)
            return formatted_json

    print("Get All User Playlists")
    offset = 0
    playlists = []
    while True:
        playlist_data = json.loads(getUserPlaylists(offset))
        if len(playlist_data['playlists']) == 0:
            break
        for playlist in playlist_data['playlists']:
            playlists.append(playlist)
        offset += 50
    
    data = {}
    data['playlists'] = playlists
    
    # implement search functionality
    if search != '':
        filtered_playlists = []
        for playlist in playlists:
            if search.lower() in playlist['name'].lower():
                filtered_playlists.append(playlist)
        result = json.loads(api.getPlaylists(search))
        for playlist in result['playlists']:
            filtered_playlists.append(playlist)
        data['playlists'] = filtered_playlists
    else:
        data['playlists'] = playlists
    json_data = data
    formatted_json = json.dumps(json_data, indent=4)
    return formatted_json
    
@app.route('/artist-songs', methods=['POST'])
def getArtistSongs():
    if request.method == 'POST':
        search = request.form['search']
        result = api.getArtistSongs(search)
        return jsonify(result)
    
@app.route('/album-songs', methods=['POST'])
def getAlbumSongs():
    if request.method == 'POST':
        search = request.form['search']
        result = api.getAlbumSongs(search)
        return jsonify(result)
    
@app.route('/playlist-songs', methods=['POST'])
def getPlaylistSongs():
    if request.method == 'POST':
        search = request.form['search']
        try:
            token_info = get_token()
        except:
            print("User not logged in")
            data = {}
            return jsonify(data)
        def getPlaylistSongs(playlistID, offset):
            print("Get Playlist Songs", playlistID, "Offset=", offset)
            sp = spotipy.Spotify(auth=token_info['access_token'])
            playlist_data = sp.playlist_items(playlistID, None, 100, offset)
            
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
                    curr_song['id'] = api.generate_id(song['track']['name'] + song['track']['album']['name'])
                else:
                    curr_song['img'] = song['track']['album']['images'][0]['url']
                songs.append(curr_song)
            
            data['songs'] = songs
            
            json_data = data
            formatted_json = json.dumps(json_data, indent=4)
            return formatted_json
        print("Get All Playlist Songs", search)
        offset = 0
        songs = []
        while True:
            playlist_data = json.loads(getPlaylistSongs(search, offset))
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
    
    
@app.route('/user-info', methods=['GET'])
def getUserInfo():
    if request.method == 'GET':
        try:
            token_info = get_token()
        except:
            print("User not logged in")
            data = {}
            return jsonify(data)
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        return jsonify(user_info)
    


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))
    
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client_id_key,
        client_secret = client_secret_key,
        redirect_uri = url_for('redirect_page', _external=True),
        scope='playlist-read-private playlist-read-collaborative user-read-private'
    )



if __name__ == '__main__':
    app.run(port=8888, debug=True)
