from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, HiddenField
from wtforms.validators import InputRequired


class BlogAddForm(FlaskForm):
    rss = StringField('RSS', validators=[InputRequired()])


class PlaceAddForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    x = IntegerField('x', validators=[InputRequired()])
    y = IntegerField('y', validators=[InputRequired()])


class PostAddForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired()])
    url = StringField('URL', validators=[InputRequired()])
    blog_id = HiddenField('Blog', validators=[InputRequired()])
    place_id = SelectField('Place', coerce=int, validators=[InputRequired()])
