from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, length

class NuggetForm(FlaskForm):
    title = StringField('', validators=[DataRequired()])
    description = TextAreaField('', validators=[DataRequired()])
    keywords = StringField('')
