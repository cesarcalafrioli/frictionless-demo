from flask_wtf import FlaskForm
from wtforms import ( StringField )

from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    url = StringField('Url do Portal de dados abertos de plataforma CKAN', validators=[InputRequired()])