from flask import Flask

from app.filters import middle
from .configs import Config
from .extensions import db, migrate
from app.user.views import user_bp
from app.blog.views import blog_bp


def create_app():
    app = Flask(__name__)
    # set configs
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    register_filters(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_filters(app):
    app.jinja_env.filters['middle'] = middle


def register_blueprints(app):
    bps = [user_bp, blog_bp]
    for bp in bps:
        app.register_blueprint(bp)
