from flask_wtf import FlaskForm
from wtforms.fields import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import data_required, email, length


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[email(), data_required()])
    username = StringField('Username', validators=[data_required(), length(5, 30)])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Login')
