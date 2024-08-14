# 아래의 줄에 jsonify 추가!
from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv

# 추가!
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError

# 추가!
from .db import db
from .ma import ma
from .models import user, post, comment

from .resources.post import Post, PostList

def create_app():
    app = Flask(__name__)
    load_dotenv(".env", verbose=True)
    app.config.from_object("config.dev")
    app.config.from_envvar("APPLICATION_SETTINGS")
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    api = Api(app)
    
    # 추가!
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    # 추가!
    @app.before_request
    def create_tables_if_necessary():
        if not hasattr(app, 'tables_created'):
            db.create_all()
            app.tables_created = True
        
    # 추가!
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    api.add_resource(PostList, "/posts/")
    api.add_resource(Post, "/posts/<int:id>")
    
    return app
