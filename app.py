from flask import Flask, render_template, request, jsonify, url_for, session, redirect
import api, db
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv


load_dotenv()
client_id_key = os.environ.get("CLIENT_ID")
client_secret_key = os.environ.get("CLIENT_SECRET")

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = os.environ.get("APP_SECRET_KEY")
TOKEN_INFO = 'token_info'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html', **locals())

@app.route('/album/<albumId>')
def album(albumId):
    albumName = api.getAlbumName(albumId)
    content_map = {
        albumId: {'id': albumId, 'title': albumName, 'type': 'album'},
    }
    default_content = {'id': albumId, 'title': 'ERROR'}
    content = None
    if albumId == '':
        content = default_content
    else:
        content = content_map.get(albumId, default_content)
    return render_template('ranker.html', **content)

@app.route('/artist/<artistId>')
def artist(artistId):
    artistName = api.getArtistName(artistId)
    content_map = {
        artistId: {'id': artistId, 'title': artistName, 'type': 'artist'},
    }
    default_content = {'id': artistId, 'title': 'ERROR'}
    content = None
    if artistId == '':
        content = default_content
    else:
        content = content_map.get(artistId, default_content)
    return render_template('ranker.html', **content)

@app.route('/playlist/<playlistId>')
def playlist(playlistId):
    playlistName = api.getPlaylistName(playlistId)
    if playlistName == '':
        try:
            token_info = get_token()
        except:
            print("User not logged in")
            return render_template('ranker.html', **{'id': playlistId, 'title': 'ERROR'})    
        sp = spotipy.Spotify(auth=token_info['access_token'])
        playlist_data = sp.playlist(playlistId)
        playlistName = playlist_data["name"]
    content_map = {
        playlistId: {'id': playlistId, 'title': playlistName, 'type': 'playlist'},
    }
    default_content = {'id': playlistId, 'title': 'ERROR'}
    content = None
    if playlistId == '':
        content = default_content
    else:
        content = content_map.get(playlistId, default_content)
    return render_template('ranker.html', **content)

@app.route('/login')
def login():
    next_url = request.args.get('next') or url_for('index')
    session['next_url'] = next_url
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    next_url = session.get('next_url')
    print("Redirecting to:", next_url)
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    with open('token.json', 'w') as file:
        json.dump(token_info, file, indent=4)
    return redirect(next_url)


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
                if playlist.get('images'):
                    if len(playlist['images']) > 0:
                        curr_playlist['img'] = playlist['images'][0]['url']
                    else:
                        curr_playlist['img'] = 'https://player.listenlive.co/templates/StandardPlayerV4/webroot/img/default-cover-art.png'
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
                if song['track'] == None:
                    continue
                curr_song = {}
                curr_song['name'] = song['track']['name']
                curr_song['id'] = song['track']['id']
                if song['track']['type'] == 'episode':
                    curr_song['date'] = "2999-12-31"
                    curr_song['album'] = song['track']['name']
                    curr_song['type'] = 'podcast'
                    curr_song['artists'] = [song['track']['show']['name']]
                    curr_song['img'] = song['track']['show']['images'][0]['url']
                    songs.append(curr_song)
                    continue
                curr_song['date'] = song['track']['album']['release_date']
                curr_song['album'] = song['track']['album']['name']
                artists = []
                for artist in song['track']['artists']:
                    artists.append(artist['name'])
                curr_song['artists'] = artists
                if song['is_local']:
                    curr_song['img'] = 'https://player.listenlive.co/templates/StandardPlayerV4/webroot/img/default-cover-art.png'
                    curr_song['id'] = api.generateID(song['track']['name'] + song['track']['album']['name'])
                    curr_song['type'] = 'local'
                else:
                    curr_song['img'] = song['track']['album']['images'][0]['url']
                    curr_song['type'] = 'spotify'
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
        
        session['logged_in'] = True
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        db.create_user(user_info)
        return jsonify(user_info)
    
    
@app.route('/save-list', methods=['POST'])
def saveList():
    if request.method == 'POST':
        data = request.json
        try:
            db.save_ranking(data)
        except:
            return jsonify({'status': 'error'})
        return jsonify({'status': 'success'})

@app.route('/load-list', methods=['POST'])
def loadList():
    if request.method == 'POST':
        user_id = request.form['user_id']
        ranking_id = request.form['ranking_id']
        result = None
        try:
            result = db.get_ranking(user_id, ranking_id)
        except:
            return jsonify({'status': 'error'})
        return jsonify(result)
    
@app.route('/feedback', methods=['POST'])
def giveFeedback():
    if request.method == 'POST':
        message = request.form['feedback']
        result = db.give_feedback(message)
        return jsonify(result)

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
