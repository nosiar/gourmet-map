from flask import render_template, request, redirect, url_for, jsonify
from . import app, db
from .models import Blog, Place, Category
from .forms import BlogAddForm, PlaceAddForm
import requests


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def list():
    blogs = Blog.query.all()
    places = Place.query.all()
    return render_template('list.html', blogs=blogs, places=places)


@app.route('/add', methods=['GET', 'POST'])
def add():
    forms = {'blog': BlogAddForm(), 'place': PlaceAddForm()}
    if forms['blog'].validate_on_submit():
        b = Blog(forms['blog'].blog_name.data, forms['blog'].url.data)
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
    x_min = request.args.get('xmin') or ''
    x_max = request.args.get('xmax') or ''
    y_min = request.args.get('ymin') or ''
    y_max = request.args.get('ymax') or ''
    places = Place.query.all()
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
