from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel

class PostSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = PostModel
        
        dump_only = [
            "author_name",
        ]
        load_only = [
            "author_id",
        ]
        
        include_fk = True
        load_instance = True
        ordered = True
        
        