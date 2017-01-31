from sqlalchemy.ext.hybrid import hybrid_method
from . import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('places', lazy='dynamic'))

    def __init__(self, name, phone, address, x, y, category):
        self.name = name
        self.phone = phone
        self.address = address
        self.x = x
        self.y = y
        self.category = category

    def __repr__(self):
        return '<Place {}>'.format(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'x': self.x,
            'y': self.y,
            'category': self.category.name
        }

    @hybrid_method
    def dist(self, x, y):
        return (self.x - x) * (self.x - x) + (self.y - y) * (self.y - y)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    url = db.Column(db.String(50), unique=True)
    rss = db.Column(db.String(50), unique=True)

    def __init__(self, name, url, rss):
        self.name = name
        self.url = url
        self.rss = rss

    def __repr__(self):
        return '<Blog {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    url = db.Column(db.String(50), unique=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog',
                           backref=db.backref('posts', lazy='dynamic'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = db.relationship('Place',
                            backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, subject, url, blog, place):
        self.subject = subject
        self.url = url
        self.blog = blog
        self.place = place

    def __repr__(self):
        return '<Post {}>'.format(self.subject)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'url': self.url,
        }
