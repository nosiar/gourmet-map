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
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('places', lazy='dynamic'))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    def __init__(self, name, x, y, category=None):
        self.name = name
        self.x = x
        self.y = y
        self.category = category

    def __repr__(self):
        return '<Place {}>'.format(self.name)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(50))

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Blog {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    url = db.Column(db.String(50))
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
