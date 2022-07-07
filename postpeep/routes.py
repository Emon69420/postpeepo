
import os
import requests
from flask import  render_template, url_for, redirect, request, session
from postpeep.forms import RegistrationForm, LoginForm, PostForm, EditProfile
from postpeep.models import User, Posts, Postlikes
from postpeep import app, database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import datetime
import smtplib
import secrets
import cloudinary
import cloudinary.uploader
from random import randint
#my_secret = os.environ['PASS']
app.secret_key = 'verysecretmotha'

cloudinary.config(
  cloud_name="postpeepbucket",
  api_key='852179146639958',
  api_secret ="Ckk8XTKWwynQyBFSuyVhkn3rxPo"
)

def generatedCode():
  code = randint(000000, 999999)
  return code

def postImage(postPictureFile):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(postPictureFile.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/post_image', picture_fn)
  i = Image.open(postPictureFile)
  i.save(picture_path)
  cloudinary.uploader.upload(picture_path,  use_filename = True, unique_filename=False)
  return picture_fn
  #os.remove(picture_path)

def saveImage(pictureFile):
  random_hex = secrets.token_hex(8)
  _, f_ext =  os.path.splitext(pictureFile.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  output_size = (100, 100)
  i = Image.open(pictureFile)
  width, height = i.size
  if width == height:    
      i.thumbnail(output_size)
      i.save(picture_path)
      cloudinary.uploader.upload(picture_path, use_filename = True, unique_filename=False )
      return picture_fn

  elif width > height:
      result = Image.new(i.mode, (width, width), 'black')
      result.paste(i, (0, (width - height) // 2))
      result.save(picture_path)
      cloudinary.uploader.upload(picture_path, use_filename = True, unique_filename=False )
      return picture_fn

  else:
     result = Image.new(i.mode, (height, height), 'black')
     result.paste(i, ((height - width) // 2, 0))
     result.save(picture_path)
     cloudinary.uploader.upload(picture_path, use_filename = True, unique_filename=False )
     return picture_fn
    
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


@app.route('/location', methods=['POST'])
def location():
  lat = request.form['lat']
  long = request.form['long']
  condition = request.form['condition']
  print(lat,long)
  payload = {'lat':lat, 'lon':long, 'apiKey': '3d11f4c6eafa418ca21c95447232a175' }
  response = requests.get('https://api.geoapify.com/v1/geocode/reverse', params=payload)
  print(response.status_code)
  print(response.json)
  area = response.json()["features"][0]["properties"]["postcode"]
  print(area)
  
  if lat == []:
    session['command'] = 1
    print(session.get('command'))
  else:
    session['command'] = 2
    print(session.get('command'))
  
  session['locality'] = area
  session['condition'] = condition
  
  return long



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
                  
  server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
  server.starttls()
  server.login("postpeepauth@yahoo.com", 'osmaksnnfoklgtix' )
  server.sendmail("postpeepauth@yahoo.com", email, message)
  
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

@app.route('/post', methods=['POST', 'GET'] )
@login_required
def post():
  form = PostForm()

  if form.validate_on_submit():
    if form.image.data:
      postedImage = postImage(form.image.data)
      print('image added')
      post_content = form.post.data
      media = postedImage
      date = datetime.datetime.now()
      post = Posts(post = post_content,media=media, date = date, user_id = current_user.get_id(), group_posted= None )
      database.session.add(post)
      database.session.commit()
      return 'Post Success'
    else:
      post_content = form.post.data
      date = datetime.datetime.now()
      post = Posts(post = post_content, media=None, date = date, user_id = current_user.get_id(), group_posted= None )
      database.session.add(post)
      database.session.commit()
      return 'Post Success'
      
    
  else:
    return render_template('post.html', form=form)

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    locality = session.get('locality', None)
    condition = session.get('condition', None)
    print(condition)
    posts  = Posts.query.filter_by(zipco = locality).order_by(Posts.date.desc()).all() 
    liked = database.session.query(Postlikes.liked_id).filter_by(liker_id = current_user.get_id()).all() 
    print(liked)

    return render_template('home.html', posts = posts, liked = liked, conditional = condition)
  

   



@app.route('/editprofile', methods=['POST','GET'])
@login_required
def editProfile():
  form = EditProfile()
  if form.validate_on_submit():
    if form.profilepicture.data:
      pictureFile = saveImage(form.profilepicture.data)
      current_user.profile_image = pictureFile
      current_user.username = form.username.data
      current_user.email = form.email.data
      database.session.commit()
    else:
      current_user.username = form.username.data
      current_user.email = form.email.data
      database.session.commit()
    return redirect(url_for('home'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  return render_template('edit.html', form = form)


@app.route('/profile/<username>', methods=['GET','POST'])
@login_required
def profilepage(username):
  user= User.query.filter_by(username=username).first()

  posts =  Posts.query.join(Postlikes).filter_by(user_id = user.id).all()

  print(posts)
  return 'hellow'
  