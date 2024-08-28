from flask_restful import Resource, request
from api.models.post import PostModel
from api.schemas.post import PostSchema
from api.models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

post_schema = PostSchema()
post_list_schema = PostSchema(many=True)

class Post(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            user = UserModel.find_by_username(get_jwt_identity())
            _post_schema = PostSchema(context={"user": user})
            return _post_schema.dump(post), 200
        else:
            return {"Error": "could not find the post."}, 404
    
    @classmethod
    @jwt_required()
    def put(cls, id):
        
        post_json = request.get_json()
        
        validate_result = post_schema.validate(post_json)
        if validate_result:
            return validate_result, 400
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        post = PostModel.find_by_id(id)
        
        if not post:
            return {"Error": "could not find the post."}, 404
        
        if post.author_id == author_id:
            post.update_to_db(post_json)
        else:
            return {"Error": "Only author can edit the post."}, 403
        
        return post_schema.dump(post), 200
    
    @classmethod
    @jwt_required()
    def delete(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            post.delete_from_db()
            return {"messages" : "Successfully deleted"}, 200
        return {"Error" : "could not find the post."}, 404
    
    
    
class PostList(Resource):
    
    @classmethod
    @jwt_required()
    def get(cls):
        user = UserModel.find_by_username(get_jwt_identity())
        page = request.args.get("page", type=int, default=1)
        _post_list_schema = PostSchema(context={"user": user}, many=True)
        
        search_querystring = f'%%{request.args.to_dict().get("search")}%%'
        if request.args.to_dict().get("search"):
            ordered_posts = PostModel.filter_by_string(
                search_querystring
            ).order_by(PostModel.id.desc())
            pagination = ordered_posts.paginate(
                page=page, per_page=10, error_out=False
                )
        return _post_list_schema.dump(pagination.items)
        
    @classmethod
    @jwt_required()
    def post(cls):
        post_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        print(author_id)
        try:
            new_post = post_schema.load(post_json)
            new_post.author_id = author_id
        except ValidationError as err:
            return err.messages, 400
        try:
            new_post.save_to_db()
        except:
            return {"Error": "Failed to save"}, 500
        return post_schema.dump(new_post), 201