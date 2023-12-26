from flask import Flask, render_template, request, jsonify, url_for, session, redirect
import api
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect


app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'YOUR_SECRET_KEY'
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
    
@app.route('/playlist', methods=['POST'])
def getPlaylists():
    if request.method == 'POST':
        search = request.form['search']
        result = api.getPlaylists(search)
        return jsonify(result)
    
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
        result = api.getAllPlaylistSongs(search)
        return jsonify(result)
    
    
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
        client_id = '15eb06a1ff0a40bd95cc7c1522c5aaa3',
        client_secret = '32ab0e56dae8427e9efe5dab273f78a4',
        redirect_uri = url_for('redirect_page', _external=True),
        scope='playlist-read-private playlist-read-collaborative user-read-private'
    )



if __name__ == '__main__':
    app.run(port=8888, debug=True)
