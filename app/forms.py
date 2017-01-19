from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class BlogAddForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    url = StringField('URL', validators=[InputRequired()])
