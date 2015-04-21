from flask_wtf import Form
from app import db
from app.models import Genre
from wtforms import SelectField, StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class GameForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    genre = SelectField('Genre', validators=[DataRequired()])
    image = FileField('Image')
    description = TextAreaField('Description', validators=[DataRequired()])
    

class DeleteForm(Form):
	submit = SubmitField('Yes, Delete it.')
