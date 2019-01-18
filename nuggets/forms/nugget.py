from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, TextAreaField
from wtforms.validators import DataRequired

class NuggetForm(FlaskForm):
    title = StringField('', validators=[DataRequired()])
    description = TextAreaField('', validators=[DataRequired()])
    keywords = StringField('')
