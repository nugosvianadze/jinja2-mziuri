from flask_wtf import FlaskForm
from wtforms.fields import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import data_required, email, length, ValidationError


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[email(), data_required()],
                       render_kw={'class': 'form-control', 'placeholder': 'Enter Email'})
    username = StringField('Username', validators=[data_required(), length(5, 30)],
                           render_kw={'class': 'form-control', 'placeholder': 'Enter Username'})
    password = PasswordField('Password', validators=[data_required()],
                             render_kw={'class': 'form-control', 'placeholder': 'Enter Password'})
    submit = SubmitField('Login')

    def validate_username(self, field):
        print(field, field.data)
        if not field.data.isalpha():
            raise ValidationError('Username Must not include numeric numbers')