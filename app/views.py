from flask import render_template, request, redirect, url_for, jsonify
from . import app, db
from .models import Blog, Place, Category
from .forms import BlogAddForm, PlaceAddForm
import requests
import feedparser
from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def list():
    blogs = Blog.query.all()
    places = Place.query.all()
    return render_template('list.html', blogs=blogs, places=places)


@app.route('/posts')
def posts():
    ee = [feedparser.parse(x.rss).entries for x in Blog.query.all()]
    entries = [e for entries in ee for e in entries]
    for e in entries:
        e.published_datetime = datetime.strptime(e.published,
                                                 '%a, %d %b %Y %H:%M:%S %z')
    entries.sort(key=lambda e: e.published_datetime, reverse=True)
    return render_template('posts.html', entries=entries)


@app.route('/add', methods=['GET', 'POST'])
def add():
    forms = {'blog': BlogAddForm(), 'place': PlaceAddForm()}
    if forms['blog'].validate_on_submit():
        rss = forms['blog'].rss.data
        f = feedparser.parse(rss)
        b = Blog(f.feed.title, f.feed.link, rss)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('add'))
    elif forms['place'].validate_on_submit():
        c = Category.query.filter_by(name=forms['place'].category.data).first()
        if c is None:
            c = Category(forms['place'].category.data)
            db.session.add(c)

        p = Place(forms['place'].name.data, forms['place'].phone.data,
                  forms['place'].address.data,
                  forms['place'].x.data, forms['place'].y.data, c)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('add.html', forms=forms)


@app.route('/delete/<id>')
def delete(id):
    redirect_to = request.referrer or url_for('index')

    try:
        id = int(id)
    except ValueError:
        return redirect(redirect_to)

    p = Place.query.get(id)
    if p is not None:
        db.session.delete(p)
        db.session.commit()

    return redirect(redirect_to)


@app.route('/json/places')
def get_places():
    x_min = request.args.get('xMin') or ''
    y_min = request.args.get('yMin') or ''
    x_max = request.args.get('xMax') or ''
    y_max = request.args.get('yMax') or ''
    x_mine = request.args.get('xMine') or ''
    y_mine = request.args.get('yMine') or ''
    places = Place.query.order_by(Place.dist(x_mine, y_mine)).all()
    #places = Place.query.filter(x_min <= Place.x and Place.x <= x_max and
    #                            y_min <= Place.y and Place.y <= y_max).all()
    return jsonify(data=[p.serialize for p in places])


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
