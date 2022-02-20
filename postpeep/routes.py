import os
from flask import  render_template, url_for, redirect, request, session
from postpeep.forms import RegistrationForm, LoginForm
from postpeep.models import User
from postpeep import app, database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import smtplib
from random import randint
my_secret = os.environ['PASS']
app.secret_key = 'verysecretmotha'

def generatedCode():
  code = randint(000000, 999999)
  return code


# All The Routes Are Here 

@app.errorhandler(404)
def not_found(e):
  return render_template("error404.html")


@app.errorhandler(500)
def server_error(e):
  return render_template("error500.html")






@app.route('/')
def hello_world():
  if current_user.is_authenticated:
    return redirect(url_for('welcome'))

  return render_template('index.html')

@app.route('/register',  methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('welcome'))
  
  

  form = RegistrationForm()
  
  if form.validate_on_submit():
    otp = generatedCode()
    session['response'] = otp
    return redirect(url_for('verify', username= form.username.data, email=form.email.data, password = form.password.data))
  else:
    return render_template('register.html', title='Register' , form=form)

@app.route('/verify/<email>/<username>/<password>', methods=['GET','POST'])
def verify(email, username, password):
  if current_user.is_authenticated:
    return redirect(url_for('welcome'))
  

  #sends mail to user  

  body= '\n your OTP is : '
  userotp = str(session.get('response', None))
  session['response'] = str(userotp)
  message = body + userotp
  print(message)
                  
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login("postpeepofficial@gmail.com", my_secret )
  server.sendmail("postpeepofficial@gmail.com", email, message)
  
  if request.method == "POST":

      enteredCode = request.form['enteredCode']
      if 'response' in session:
        s= session['response']
        session.pop('response', None)
        if int(enteredCode) == int(s):

          #gets value from form and hashes it
          hashed_password =  bcrypt.generate_password_hash(password).decode('utf-8')
          #adds value to database table, here User is the class of database model
          user = User(username=username, email=email, password=hashed_password, registration_date= datetime.datetime.now())
          database.session.add(user)
          database.session.commit()
          return redirect(url_for('login'))          
        
        else:
          
          return render_template('failedverification.html')
  
  return render_template('verification.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('welcome'))
  
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, True)
      next_page = request.args.get('next')
      print(next_page)
      #return redirect(url_for(next_page)) if next_page else redirect(url_for('welcome'))
      return redirect(url_for('welcome'))
    else:
      return render_template('failedlogin.html', form=form, title = 'login')

  else:
    return render_template('login.html', title='login', form=form )

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('register'))


@app.route("/welcome")
@login_required
def welcome():
  return render_template('welcome.html', title = 'welcome')