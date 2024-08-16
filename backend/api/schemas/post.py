from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel

class PostSchema(ma.SQLAlchemyAutoSchema):
    
    author_name = Method("get_author_name")
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.username
        return None
    
    class Meta:
        model = PostModel
        
        dump_only = [
            "author_name",
        ]
        
        exclude = ("author_id",)
        
        include_fk = True
        load_instance = True
        ordered = True
        
        