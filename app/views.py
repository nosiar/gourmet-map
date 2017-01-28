from flask import render_template, request, redirect, url_for, jsonify
from . import app, db
from .models import Blog, Place, Category, Post
from .forms import BlogAddForm, PlaceAddForm, PostAddForm
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
    posts = Post.query.all()
    return render_template('list.html', blogs=blogs, places=places,
                           posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    forms = {'blog': BlogAddForm(),
             'place': PlaceAddForm(),
             'post': PostAddForm()}
    forms['post'].place_id.choices = [(p.id, p.name)
                                      for p in Place.query.order_by('name')]

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
    elif forms['post'].validate_on_submit():
        form = forms['post']
        b = Blog.query.get(form.blog_id.data)
        p = Place.query.get(form.place_id.data)
        Post(form.subject.data, form.url.data, b, p)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('add'))

    blogs = Blog.query.all()
    entries = []
    for b in blogs:
        sub_entries = feedparser.parse(b.rss).entries
        for e in sub_entries:
            e.blog_id = b.id
            e.pub_datetime = datetime.strptime(e.published,
                                               '%a, %d %b %Y %H:%M:%S %z')
        entries.extend(sub_entries)
    entries.sort(key=lambda e: e.pub_datetime, reverse=True)

    return render_template('add.html', entries=entries, forms=forms)


@app.route('/delete/place/<place_id>')
@app.route('/delete/post/<post_id>')
def delete(place_id=None, post_id=None):
    redirect_to = request.referrer or url_for('index')

    if place_id is not None:
        try:
            id = int(place_id)
        except ValueError:
            return redirect(redirect_to)

        p = Place.query.get(id)
        if p is not None:
            db.session.delete(p)
            db.session.commit()
    elif post_id is not None:
        try:
            id = int(post_id)
        except ValueError:
            return redirect(redirect_to)

        p = Post.query.get(id)
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
