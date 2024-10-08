from api.ma import ma
from marshmallow.fields import String
from marshmallow import validates_schema, post_dump
from marshmallow.exceptions import ValidationError
from api.models.user import UserModel
from marshmallow import fields

fields.Field.default_error_messages["required"] = "This field cannot be blank."
fields.Field.default_error_messages["validator_failed"] = "Validation failed."
fields.Field.default_error_messages["null"] = "This field cannot be null."

class UserRegisterSchema(ma.SQLAlchemyAutoSchema):
    password_confirm = String(required=True)
    class Meta:
        load_instance = True
        model = UserModel
        load_only = [
            "username",
            "email",
            "password",
            "password_confirm",
        ]
    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["password_confirm"]:
            raise ValidationError("Incorrect password.", "password_confirm")
        
class AuthorSchema(ma.SQLAlchemyAutoSchema):
    
    @post_dump
    def set_default_image(self, data, **kawrgs):
        if data["image"] == "" or data["image"] == None:
            data["image"] = "default/default.jpg"
        return data
    
    class Meta:
        model = UserModel
        exclude = (
            "password",
            "created_at",
            "email",
        )
        
class UserSchema(ma.SQLAlchemyAutoSchema):
    image = String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d")
    
    @post_dump
    def set_default_image(self, data, **kwargs):
        if data["image"] == "" or data["image"] == None:
            data["image"] = "default/default.jpg"
        return data
    
    class Meta:
        model = UserModel
        exclude = ("password",)
        dump_only = ("email", "username")