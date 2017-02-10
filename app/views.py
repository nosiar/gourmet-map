from flask import render_template, request, redirect, url_for, jsonify
from sqlalchemy import desc
from . import app, db
from .models import Blog, Place, Category, Post, PostCandidate, LastRead
from .forms import BlogAddForm, PlaceAddForm, PostAddForm
import requests
import feedparser
from datetime import datetime
from time import mktime


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


def parse(rss):
    if 'egloos' in rss:
        rss = requests.get(rss).text
    return feedparser.parse(rss)


def filter(subject):
    exclude = ['후쿠오카', '성수동', 'Domaine']
    for e in exclude:
        if e in subject:
            return False
    return True


def add_post_candidates():
    blogs = Blog.query.all()
    for b in blogs:
        last_read = LastRead.query.filter_by(blog_id=b.id).first()
        if last_read is None:
            last_read = LastRead(b.id)
            db.session.add(last_read)

        day_diff = (datetime.now() - last_read.date).days
        if day_diff == 0:
            continue

        sub_entries = parse(b.rss).entries
        for e in sub_entries:

            date = datetime.fromtimestamp(mktime(e.published_parsed))
            if date < last_read.date:
                break
            if not filter(e.title):
                continue
            p = PostCandidate(e.title, e.link, date, b.id)
            db.session.add(p)
        last_read.date = datetime.now()
    db.session.commit()


@app.route('/add', methods=['GET', 'POST'])
def add():
    forms = {'blog': BlogAddForm(),
             'place': PlaceAddForm(),
             'post': PostAddForm()}
    forms['post'].place_id.choices = [(p.id, p.name)
                                      for p in Place.query.order_by('name')]

    if forms['blog'].validate_on_submit():
        rss = forms['blog'].rss.data
        f = parse(rss)
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

    add_post_candidates()

    posts = PostCandidate.query.order_by(desc(PostCandidate.date)).all()

    return render_template('add.html', posts=posts, forms=forms)


@app.route('/delete/place/<place_id>')
@app.route('/delete/post/<post_id>')
@app.route('/delete/candidate/<candidate_id>')
def delete(place_id=None, post_id=None, candidate_id=None):
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
    elif candidate_id is not None:
        try:
            id = int(candidate_id)
        except ValueError:
            return redirect(redirect_to)

        p = PostCandidate.query.get(id)
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


@app.route('/json/posts')
def get_posts():
    place_id = request.args.get('place_id') or ''
    posts = Post.query.filter_by(place_id=place_id).all()
    return jsonify(data=[p.serialize for p in posts])


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
