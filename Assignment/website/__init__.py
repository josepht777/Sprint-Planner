from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this key holds session and cookie data'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix = '/') #this is the prefix bere any of the route in the views in the views file

    from .models import Task, Sprint, User

    create_database(app)

    return app

#creates dataBase if it does not exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)