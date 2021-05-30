from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from flask_wtf.file import FileField
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    broker = StringField('Broker', validators=[DataRequired()])
    submit = SubmitField('Continue!')

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.

class MarkForm(FlaskForm):
    # mark_list = SelectMultipleField('Broker', validators=[DataRequired()], choices=[], render_kw={'data-mdb-filter': True})
    submit = SubmitField('Continue!')