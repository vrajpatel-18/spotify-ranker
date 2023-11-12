from flask import Flask, render_template, request, jsonify
import api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', **locals())

@app.route('/ranker')
def ranker():
    return render_template('ranker.html', **locals())


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



if __name__ == '__main__':
    app.run(port=8888, debug=True)
