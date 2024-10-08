from api.models.user import UserModel, RefreshTokenModel
from api.models.post import PostModel
from flask_restful import Resource, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from flask.views import MethodView
from werkzeug.security import check_password_hash
from api.schemas.user import UserRegisterSchema, UserSchema
import random

register_schema = UserRegisterSchema()
user_schema = UserSchema()
user_list_schema = UserSchema(many=True, exclude=["email", "created_at"])

class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        validate_result = register_schema.validate(data)
        if validate_result:
            return validate_result, 400
        else:
            if UserModel.find_by_username(data["username"]):
                return {"bad request": "This username already exist."}, 400
            elif UserModel.find_by_email(data["email"]):
                return {"message": "This email already exist."}, 400
            else:
                password = generate_password_hash(data["password"])
                user = register_schema.load(
                    {
                        "username": data["username"],
                        "email": data["email"],
                        "password": password,
                        "password_confirm": password,
                    }
                )
            user.save_to_db()
            return {"success": f"{user.username}!"}, 201
        
class UserLogin(MethodView):
    
    def post(self):
        data = request.get_json()
        user = UserModel.find_by_email(data["email"])
        
        additional_claims = {"user_id": user.id}
        
        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(
                identity=user.username, 
                fresh=True,
                additional_claims=additional_claims
                )
            refresh_token = create_refresh_token(
                identity=user.username,
                additional_claims=additional_claims
                )
            # if refresh token exists for username, update, otherwise save
            if user.token:
                token = user.token[0]
                token.refresh_token_value = refresh_token
                token.save_to_db()
            else:
                new_token = RefreshTokenModel(user_id=user.id, refresh_token_value=refresh_token)
                new_token.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        return {"Unauthorized": "Check your email and password"}, 401
    
class RefreshToken(MethodView):
    """
    Receive Refresh Token and verify
    New Refresh Token and Access Token
    Since Refresh Token is one-time only, when new refresh token is received,
    save its value in db
    """
    @jwt_required(refresh=True)
    def post(self):
        """
        assume refresh token is verified,
        if user's existing refresh token is different than post refresh token,
        access token must be failed
        """
        identity = get_jwt_identity()
        token = dict(request.headers)["Authorization"][7:]
        user = RefreshTokenModel.get_user_by_token(token)
        if not user:
            return {"Unauthorized": "Refresh token cannot be used more than twice"}, 401
        # access token, refresh token
        additional_claims = {"user_id": user.id}
        
        access_token = create_access_token(
            identity=identity,
            fresh=True,
            additional_claims=additional_claims,
            )
        refresh_token = create_refresh_token(
            identity=user.username,
            additional_claims=additional_claims,
            )
        if user:
            token = user.token[0]
            token.refresh_token_value = refresh_token
            token.save_to_db()
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
class MyPage(Resource):
    
    @classmethod
    @jwt_required()
    def get():
        
        username = get_jwt_identity()
        user = UserModel.find_by_username(username=username)
        if not user:
            return {"Error": "could not find user."}, 404
        if id == user.id:
            return user_schema(user), 200
        return {"Error": "Invalid."}, 403
    
    @classmethod
    @jwt_required()
    def put():
        
        user_json = request.get_json()
        validate_result = user_schema.validate(user_json)
        if validate_result:
            return validate_result, 400
        
        user = UserModel.find_by_username(get_jwt_identity())
        
        if not user:
            return {"Error": "could not find user."}, 404
        request_user = UserModel.find_by_username(get_jwt_identity())
        
        if id == request_user.id:
            user.update_to_db(user_json)
            return user_schema.dump(user)
        else:
            return {"Error": "Invalid."}, 403
        
class PostLike(Resource):
    
    @classmethod
    @jwt_required()
    def put(cls, id):
        
        user = UserModel.find_by_username(get_jwt_identity())
        post = PostModel.find_by_id(id)
        if not user or not post:
            return {"Error": "Invalid."}, 400
        post.do_like(user)
        return post.get_liker_count(), 200
    
    @classmethod
    @jwt_required()
    def delete(cls, id):
        
        user = UserModel.find_by_username(get_jwt_identity())
        post = PostModel.find_by_id(id)
        if not user or not post:
            return {"Error": "Invalid."}, 400
        post.cancel_like(user)
        return post.get_liker_count(), 200
    
class Follow(Resource):
    
    @classmethod
    @jwt_required()
    def put(cls, id):
        request_user = UserModel.find_by_username(get_jwt_identity())
        user_to_follow = UserModel.find_by_id(id)
        if not request_user:
            return {"error": "User not found."}, 400
        if id == get_jwt().get("user_id"):
            return {"error": "Cannot follow yourself."}, 400
        request_user.follow(user_to_follow)
        return "", 204
    
    @classmethod
    @jwt_required()
    def delete(cls, id):
        request_user = UserModel.find_by_username(get_jwt_identity())
        user_to_follow = UserModel.find_by_id(id)
        if not request_user:
            return {"error": "User not found."}, 400
        if id == get_jwt().get("user_id"):
            return {"error": "Cannot follow yourself."}, 400
        request_user.unfollow(user_to_follow)
        return "", 204
    
class Recommend(Resource):
    
    @classmethod
    @jwt_required()
    def get(cls):
        request_user = UserModel.find_by_username(get_jwt_identity())
        return user_list_schema.dump(
            random.sample(
                list(
                    set(UserModel.query.all())
                    - set([request_user])
                    - set(request_user.followed.all())
                ),
                2,
            )
        )