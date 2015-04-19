from flask_wtf import Form
from app import db
from app.models import Genre
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired

class GameForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    genre = SelectField('Genre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
