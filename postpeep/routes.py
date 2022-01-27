from flask import  render_template, url_for, redirect, request
from postpeep.forms import RegistrationForm, LoginForm
from postpeep.models import User
from postpeep import app, database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import datetime


# All The Routes Are Here 
@app.route('/')
def hello_world():
  return '<h1>Hello, World!</h1>'

@app.route('/register',  methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('welcome'))
  form = RegistrationForm()
  if form.validate_on_submit():
    #gets value from form and hashes it
    hashed_password =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #adds value to database table, here User is the class of database model
    user = User(username=form.username.data, email=form.email.data, password=hashed_password, registration_date= datetime.datetime.now())
    database.session.add(user)
    database.session.commit()
    return redirect(url_for('login'))
  else:
    return render_template('register.html', title='Register' , form=form)

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