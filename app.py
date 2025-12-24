from flask import Flask
from extensions import db, login_manager, oauth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.setdefault('GOOGLE_CLIENT_ID', os.getenv('GOOGLE_CLIENT_ID'))
    app.config.setdefault('GOOGLE_CLIENT_SECRET', os.getenv('GOOGLE_CLIENT_SECRET'))

    if test_config:
        app.config.update(test_config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    oauth.init_app(app)
    app.config['GOOGLE_LOGIN_ENABLED'] = False

    client_id = app.config.get('GOOGLE_CLIENT_ID')
    client_secret = app.config.get('GOOGLE_CLIENT_SECRET')
    if client_id and client_secret:
        oauth.register(
            name='google',
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        app.config['GOOGLE_LOGIN_ENABLED'] = True

    # Register Blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
