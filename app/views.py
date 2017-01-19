from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Blog
from .forms import BlogAddForm
import requests


@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BlogAddForm()
    if form.validate_on_submit():
        b = Blog(form.name.data, form.url.data)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('add.html', form=form)


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
