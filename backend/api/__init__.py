# 아래의 줄에 jsonify 추가!
from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from datetime import timedelta
from flask_uploads import configure_uploads
# 추가!
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError

from flask_cors import CORS

# 추가!
from .db import db
from .ma import ma
from .models import user, post, comment

from .resources.post import Post, PostList
from .resources.user import UserRegister, UserLogin, RefreshToken
from .resources.image import ImageUpload, Image
from .resources.comment import CommentDetail, CommentList
from api.utils.image_upload import IMAGE_SET

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    load_dotenv(".env", verbose=True)
    app.config.from_object("config.dev")
    app.config.from_envvar("APPLICATION_SETTINGS")
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.config["JSON_AS_ASCII"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)    
    api = Api(app)
    
    configure_uploads(app, IMAGE_SET)
    
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

    # resources
    api.add_resource(PostList, "/posts/")
    api.add_resource(Post, "/posts/<int:id>")
    api.add_resource(UserRegister, "/register/")
    api.add_resource(UserLogin, "/login/")
    api.add_resource(RefreshToken, "/refresh/")
    api.add_resource(ImageUpload, "/upload/image/")
    api.add_resource(Image, "/statics/<path:path>")
    api.add_resource(CommentList, "/posts/<int:post_id>/comments/")
    api.add_resource(CommentDetail, "/posts/<int:post_id>/comments/<int:comment_id>/")
    
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"Error": "Token is expired"}),
            401,
        )
        
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"Error", "Invalid Token"}),
            401,
        )
        
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"Error": "Unauthorized Token"}),
            401,
        )
    
    return app
