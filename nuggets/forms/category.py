from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, length

class CategoryForm(FlaskForm):
    label = StringField('', validators=[DataRequired(), length(max=64)])
    status = SelectField('', choices=[(0, 'Active'), (1, 'Inactive')])
