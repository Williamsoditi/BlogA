from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import User

class SignupForm(FlaskForm):
    email = StringField('Your Email Address',validators=[DataRequired(),Email()])
    name = StringField('Enter Your Username')
    password = PasswordField('Password' ,validators = [EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords')
    submit = SubmitField('Create account')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("There is an account with that email")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("That username is taken")

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me!')
    submit = SubmitField('Sign In')