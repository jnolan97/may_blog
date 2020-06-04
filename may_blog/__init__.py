from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Import for Flask Mail
from flask_mail import Mail, Message

#Import for flask login
from flask_login import LoginManager
# Create flask app variable
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

login = LoginManager(app)
login.login_view = 'login' # Specify what page to load for NON-authenticated Users


from may_blog import routes,models
