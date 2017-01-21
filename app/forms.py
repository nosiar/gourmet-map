from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired


class BlogAddForm(FlaskForm):
    blog_name = StringField('Name', validators=[InputRequired()])
    url = StringField('URL', validators=[InputRequired()])


class PlaceAddForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    x = IntegerField('x', validators=[InputRequired()])
    y = IntegerField('y', validators=[InputRequired()])
