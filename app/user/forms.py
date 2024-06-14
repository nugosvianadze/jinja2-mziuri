from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField
from wtforms.fields import EmailField, StringField, PasswordField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import data_required, email, ValidationError, InputRequired

from enums import RoleEnum


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[email(), data_required()],
                       render_kw={'class': 'form-control', 'placeholder': 'Enter Email'})
    password = PasswordField('Password', validators=[data_required()],
                             render_kw={'class': 'form-control', 'placeholder': 'Enter Password'})
    submit = SubmitField('Login')

    def validate_username(self, field):
        print(field, field.data)
        if not field.data.isalpha():
            raise ValidationError('Username Must not include numeric numbers')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[email(), data_required()],
                       render_kw={'class': 'form-control', 'placeholder': 'Enter Email'})
    password = PasswordField('Password', validators=[data_required()],
                             render_kw={'class': 'form-control', 'placeholder': 'Enter Password'})
    first_name = StringField('First Name', validators=[data_required()],
                             render_kw={'class': 'form-control', 'placeholder': 'Enter First Name'})
    last_name = StringField('Last Name', validators=[data_required()],
                            render_kw={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    age = IntegerField('Age', validators=[data_required()],
                       render_kw={'class': 'form-control', 'placeholder': 'Enter Age'})
    profile_picture = FileField('Profile Picture',
                                validators=[FileAllowed(['jpg', 'png', 'svg', 'jpeg'])])
    address = StringField('Address',
                          render_kw={'class': 'form-control', 'placeholder': 'Enter Address'})
    roles = SelectMultipleField('Roles',
                                choices=[(role.value, role.name) for role in RoleEnum])
    submit = SubmitField('Sign In', render_kw={'class': 'btn btn-primary'})


def validate_id_number(form, field):
    print(field.data > 99999999999)
    if field.data > 99999999999:
        raise ValidationError('Id Number Must Not be more than 11 letter')


class UserUpdateForm(RegistrationForm):
    birthday = None
    email = None
    password = None
    id_number = IntegerField('Id Number', [InputRequired(), validate_id_number])
