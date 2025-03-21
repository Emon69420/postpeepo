from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp
from postpeep.models import User

class RegistrationForm(FlaskForm):

  username = StringField('username',  validators =[InputRequired(),  Regexp("^[0-9A-Za-z_.]+$", message='only numbers, letters, underscores and periods are allowed'), Length(min=2, max=20)])
  email = StringField('email', validators =[InputRequired()])
  password = PasswordField('Password', validators =[InputRequired()])
  submit = SubmitField('register')

  def validate_username(self, username):
    
    user= User.query.filter_by(username=username.data).first()

    if user:
      raise ValidationError('username taken, please choose a different one')

  def validate_email(self, email):
    
    email = User.query.filter_by(email=email.data).first()

    if email:
      raise ValidationError('email already registered')

class LoginForm(FlaskForm):



  email = StringField('email', validators=[InputRequired()])
  password = PasswordField('Password',validators=[InputRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('sign in')


#custom error template
  ''' def validate_stuff(self, stuff):
    
    stuff and all the operations needed to be performed
    
    if stuff:
      raise ValidationError('error message')'''

class VerificationForm(FlaskForm):

  verification = IntegerField('Enter OTP', validators=[InputRequired()])
  submit = SubmitField('Submit OTP')
  