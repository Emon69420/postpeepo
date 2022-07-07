from postpeep import database, login_manager
from flask_login import UserMixin
# database models
# same rows as user table

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))



class Usergroup(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    group_id = database.Column(database.Integer, database.ForeignKey('groups.id'), nullable= False)
    member_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable = False)
    mod = database.Column(database.Integer,unique= False, nullable = False)
    user_relation = database.relationship("User")
    group_relation = database.relationship("Groups")
  
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(30), unique=True, nullable=False)
    password = database.Column(database.String(60),unique=False,nullable=False)
    email = database.Column(database.String(256), unique=True, nullable=False)
    
    registration_date = database.Column(database.String(12), unique=False, nullable=True)
    profile_image = database.Column(database.String(20), unique=False, nullable=True)
    post =  database.relationship('Posts', backref='author', lazy=True)
    group = database.relationship('Groups', backref='creator', lazy= True)
    member = database.relationship('Usergroup', backref = 'member', lazy = True )
    likerelation =  database.relationship('Postlikes', backref = 'liker', lazy = True)
  
    # defines how data is represented when queried from database 
    def __repr__(self):
      return f"User('{self.username}', '{self.email}', '{self.registration_date}', '{self.profile_image}')"


class Groups(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    unique_name = database.Column(database.String(30), unique=True, nullable=False)
    group_name = database.Column(database.String(30), unique= False, nullable= False)
    date = database.Column(database.String(12), unique = False, nullable = False)
    created_by = database.Column(database.Integer, database.ForeignKey('user.id'), nullable = False)
    posted = database.relationship('Posts', backref = 'group', lazy= True)
    userrelation = database.relationship('Usergroup', backref = 'groupin', lazy = True )
    #likerelation =  database.relationship('Postlikes', backref = 'liker', lazy = True)
    #user_relation = database.relationship('User', backref =  "creator", lazy = True)

    # defines how data is represented when queried from database 
    def __repr__(self):
      return f"Groups('{self.unique_name}', '{self.group_name}')"


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post = database.Column(database.String(300), unique=False, nullable=False)
    date = database.Column(database.String(12), unique=False, nullable=False)
    media = database.Column(database.String(60), unique = True, nullable=True)
    zipco = database.Column(database.Integer, unique = False, nullable = False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    group_posted = database.Column(database.Integer, database.ForeignKey('groups.id'), nullable = True)
    postlikerelation =  database.relationship('Postlikes', backref = 'liked', lazy = True)
    # defines how data is represented when queried from database 
    def __repr__(self):
      return f"User('{self.post}', '{self.date}')"


class Postlikes(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    liker_id =  database.Column(database.Integer, database.ForeignKey('user.id'), nullable = False)
    liked_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable =  False)