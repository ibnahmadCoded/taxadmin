import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
DB_NAME = os.getenv("DB_NAME")

with open(os.getenv("SECRET_KEY_PATH"), 'r') as file:
    secret_key = file.read().strip()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User
    from .admin_views import setup_admin
    from .views import views
    from .auth import auth

    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        # Check if the superuser exists, create if not
        superuser = User.query.filter_by(username='admin').first()
        if not superuser:
            superuser = User(username='admin', email='admin@example.com')
            superuser.set_password('password123')  # Hash the password
            superuser.is_superuser = True  # Set the is_superuser field to True
            db.session.add(superuser)
            db.session.commit()

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    setup_admin(app)

    return app