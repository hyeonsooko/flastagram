from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel
from marshmallow import Schema, fields
from api.schemas.user import AuthorSchema

class PostSchema(ma.SQLAlchemyAutoSchema):
    
    image = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d, %H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m-%d, %H:%M:%S")
    author = fields.Nested(AuthorSchema)
    liker_count = Method("get_liker_count")
    is_like = Method("get_is_like")
    
    def get_liker_count(self, obj):
        return obj.get_liker_count()
    
    def get_is_like(self, obj):
        return obj.is_like(self.context["user"])
    
    class Meta:
        model = PostModel
        
        dump_only = [
            "author_name",
            "is_like",
        ]
        
        exclude = ("author_id",)
        
        include_fk = True
        load_instance = True
        ordered = True
        
        