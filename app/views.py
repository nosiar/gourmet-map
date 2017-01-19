from flask import render_template, request
from . import app
import requests


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    client_id = 'WuHk4eJpsqDQ5tLWjYbi'
    client_secret = 'GuoH_Irsnd'
    url = 'https://openapi.naver.com/v1/search/local.json'
    query = request.args.get('query')

    r = requests.get(url,
                     params={'query': query},
                     headers={'X-Naver-Client-Id': client_id,
                              'X-Naver-Client-Secret': client_secret})

    return r.text
