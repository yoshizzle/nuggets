from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, length

class TemplateForm(FlaskForm):
    label = StringField('', validators=[DataRequired(), length(max=64)])
    logo_url = StringField('')
    status = SelectField('', choices=[(1, 'Active'), (0, 'Inactive')])
    summary = StringField('', validators=[DataRequired()])
    description = TextAreaField('', validators=[DataRequired()])
    version = StringField('', validators=[DataRequired()])
    base_price = StringField('', validators=[DataRequired()])
    category = SelectField('', choices=[])

    @classmethod
    def gen_categories(cls, values):
        """
        This class method populates the choices for the category selectors
        """
        values = [('', '-- Please Choose --')] + values
        setattr(cls, 'category', SelectField('', choices=values))
        return cls
