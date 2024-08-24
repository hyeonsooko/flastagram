from api.ma import ma, Method
from api.models.comment import CommentModel
from marshmallow import fields

class CommentSchema(ma.SQLAlchemyAutoSchema):
    
    created_at = fields.DateTime(format="%Y-%m-%d, %H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m-%d, %H:%M:%S")
    
    author_name = Method("get_author_name")
    
    def get_author_name(self, obj):
        return obj.author.username
    
    class Meta:
        model = CommentModel
        dump_only = [
            "author_name",
        ]
        exclude = ("author_id", "post_id")
        load_instance = True
        include_fk = True
        ordered = True
        