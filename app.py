from flask import Flask, render_template, request, jsonify, url_for, session, redirect
from flask_talisman import Talisman
from flask_session import Session
from redis import Redis
import api, db
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from dotenv import load_dotenv


load_dotenv()
client_id_key = os.environ.get("CLIENT_ID")
client_secret_key = os.environ.get("CLIENT_SECRET")

app = Flask(__name__)
Talisman(app, content_security_policy=None)

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis.from_url(
    os.environ.get('REDIS_URL'), ssl_cert_reqs=None
)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)  # Set up Flask-Session

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = os.environ.get("APP_SECRET_KEY")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/token')
def token():
    user_id = session.get('user_id')
    return session.get(f'{user_id}_token')

@app.route('/player')
def player():
    return render_template('player.html', **locals())

@app.route('/')
def index():
    get_token()
    return render_template('index.html', **locals())

@app.route('/album/<albumId>')
def album(albumId):
    albumName = api.getAlbumName(albumId)
    content_map = {
        albumId: {'id': albumId, 'title': albumName, 'type': 'album'},
    }
    default_content = {'id': albumId, 'title': 'ERROR'}
    content = content_map.get(albumId, default_content)
    return render_template('ranker.html', **content)

@app.route('/artist/<artistId>')
def artist(artistId):
    artistName = api.getArtistName(artistId)
    content_map = {
        artistId: {'id': artistId, 'title': artistName, 'type': 'artist'},
    }
    default_content = {'id': artistId, 'title': 'ERROR'}
    content = content_map.get(artistId, default_content)
    return render_template('ranker.html', **content)

@app.route('/playlist/<playlistId>')
def playlist(playlistId):
    playlistName = api.getPlaylistName(playlistId)
    if playlistName == '':
        try:
            token_info = get_token(user_specific=True)
            if not token_info:
                print("User not logged in")
                return render_template('ranker.html', **{'id': playlistId, 'title': 'ERROR'})
            sp = spotipy.Spotify(auth=token_info['access_token'])
            playlist_data = sp.playlist(playlistId)
            playlistName = playlist_data["name"]
        except:
            print("Failed to get user-specific playlist")
            return render_template('ranker.html', **{'id': playlistId, 'title': 'ERROR'})
    content_map = {
        playlistId: {'id': playlistId, 'title': playlistName, 'type': 'playlist'},
    }
    content = content_map.get(playlistId, {'id': playlistId, 'title': 'ERROR'})
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
    code = request.args.get('code')
    print(f"Authorization code: {code}")
    
    # Get access token from Spotify
    token_info = create_spotify_oauth().get_access_token(code)
    print(f"Token info: {token_info}")

    # Get user information from Spotify
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()

    if not user_info:
        print("User info not retrieved. Redirecting to login.")
        return redirect(url_for('login'))

    # Store user ID and token in the session
    user_id = user_info['id']
    session.clear()  # Clear session except next_url
    session['next_url'] = next_url
    session['user_id'] = user_id
    session[f'{user_id}_token'] = token_info
    print(f"Session data after login: {session}")

    # Redirect to the next page
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
            token_info = get_token(user_specific=True)
            if not token_info:
                print("User not logged in")
                if search == '':
                    return jsonify({})  # Return empty data if search is empty
                else:
                    result = api.getPlaylists(search)  # Call your API to get playlists
                    return jsonify(result)  # Return the result
        except Exception as e:
            print(f"Failed to get token or playlists: {e}")
            return jsonify({'error': 'Failed to retrieve playlists'}), 500  # Return an error response


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
            return jsonify({})
        return jsonify(api.getPlaylistSongs(search))

@app.route('/user-info', methods=['GET'])
def getUserInfo():
    token_info = get_token(user_specific=True)
    
    if not token_info or 'refresh_token' not in token_info:
        print("User not logged in or invalid token")
        return redirect(url_for('login'))

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
        print(f"Client credentials token request failed with status code {auth_response.status_code}")
        return None

def get_token(user_specific=False):
    user_id = session.get('user_id')
    token_info = session.get(f'{user_id}_token', None)
    
    if not token_info:
        if user_specific:
            print("No user-specific token found, returning None")
            return None
        else:
            token_info = create_client_credentials_token()
            if token_info:
                session[f'{user_id}_token'] = token_info
            else:
                print("Failed to create default token")
                return None

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60

    if is_expired:
        print("Token expired, refreshing token")
        if 'refresh_token' in token_info:
            spotify_oauth = create_spotify_oauth()
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
            session[f'{user_id}_token'] = token_info
        else:
            token_info = create_client_credentials_token()
            session[f'{user_id}_token'] = token_info

    return token_info

  

@app.route('/check-session')
def check_session():
    return jsonify(dict(session))



def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client_id_key,
        client_secret = client_secret_key,
        redirect_uri = url_for('redirect_page', _external=True),
        scope='playlist-read-private playlist-read-collaborative user-read-private'
    )


if __name__ == '__main__':
    app.run(port=8888, debug=True)
