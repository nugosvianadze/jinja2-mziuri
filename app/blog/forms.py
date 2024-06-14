from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import data_required


class PostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის სათაური', 'class': 'form-control'})
    content = TextAreaField('Content    ', validators=[data_required()],
                        render_kw={'placeholder': 'შეიყვანეთ პოსტის კონტენტი', 'class': 'form-control'})
    submit = SubmitField('Create Post', render_kw={'class': 'btn btn-primary', 'style': 'text-align: center;'})
