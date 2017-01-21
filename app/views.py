from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Blog, Place, Category
from .forms import BlogAddForm, PlaceAddForm
import requests


@app.route('/')
def index():
    blogs = Blog.query.all()
    places = Place.query.all()
    return render_template('index.html', blogs=blogs, places=places)


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
                  forms['place'].x.data, forms['place'].y, c)
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
