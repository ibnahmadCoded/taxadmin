import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = os.getenv("DB_NAME")

# Define the path to your secret key file
#secret_key_file = os.getenv("SECRET_KEY_PATH")

# Read the secret key from the file
with open(os.getenv("SECRET_KEY_PATH"), 'r') as file:
    secret_key = file.read().strip()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import setup_admin

    # Create the database
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Set up the admin interface
    setup_admin(app)

    return app
