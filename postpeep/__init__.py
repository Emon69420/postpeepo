from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = '77869e944840a66f71edb77198e2d374'

#database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://u7izmd0xnbgzf72n:rLY6MVxtSEM1jK5Bp5ox@bcukcrmqqjt7awyhvdvp-mysql.services.clever-cloud.com:3306/bcukcrmqqjt7awyhvdvp"
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from postpeep import routes