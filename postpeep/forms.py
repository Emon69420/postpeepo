from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import  InputRequired, Length, ValidationError, Regexp 
from postpeep.models import User
from flask_login import current_user

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


class PostForm(FlaskForm):

  post = StringField('Write Something!', validators=[InputRequired()])
  image = FileField('Add an image', validators=[FileAllowed(['jpg','png','gif', 'jpeg'])])
  submit = SubmitField('post!')

class EditProfile(FlaskForm):
  username = StringField('New Username', validators =[InputRequired(),  Regexp("^[0-9A-Za-z_.]+$", message='only numbers, letters, underscores and periods are allowed'), Length(min=2, max=20)])
  email = StringField('Email', validators =[InputRequired()])
  profilepicture = FileField('Profile Picture', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
  update = SubmitField('Update')

  def validate_username(self, username):
    if username.data != current_user.username:
      user= User.query.filter_by(username=username.data).first()

      if user:
        raise ValidationError('username taken, please choose a different one')
  def validate_email(self, email):
    if email.data != current_user.email :
      email = User.query.filter_by(email=email.data).first()

      if email:
        raise ValidationError('email already registered')
      
      