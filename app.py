from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', **locals())

@app.route('/ranker')
def ranker():
    return render_template('ranker.html', **locals())

if __name__ == '__main__':
    app.run(port=8888, debug=True)
