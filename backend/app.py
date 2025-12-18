from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    from routes.auth import auth_bp
    from routes.posts import posts_bp
    from routes.feed import feed_bp
    from routes.social import social_bp
    from routes.likes import like_bp
    from routes.comments import comment_bp
    from routes.profile import profile_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(like_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(social_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)