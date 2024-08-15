from api.models.user import UserModel
from flask_restful import Resource, request
from werkzeug.security import generate_password_hash
from api.schemas.user import UserRegisterSchema
register_schema = UserRegisterSchema()

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