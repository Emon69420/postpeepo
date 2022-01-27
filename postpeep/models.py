from postpeep import database, login_manager
from flask_login import UserMixin
# database models
# same rows as user table

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(30), unique=True, nullable=False)
    password = database.Column(database.String(60),unique=False,nullable=False)
    email = database.Column(database.String(256), unique=True, nullable=False)
    registration_date = database.Column(database.String(12), unique=False, nullable=True)
    profile_image = database.Column(database.String(20), unique=False, nullable=True)
     
    # defines how data is represented when queried from database 
    def __repr__(self):
      return f"User('{self.username}', '{self.email}', '{self.registration_date}', '{self.profile_image}')"