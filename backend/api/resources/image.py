from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.utils import image_upload
from api.schemas.image import ImageSchema

import os
import traceback

image_schema = ImageSchema()

class ImageUpload(Resource):
    
    @jwt_required()
    def post(self):
        data = image_schema.load(request.files)
        print(data)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_upload.save_image(data["image"], folder=folder)
            basename = image_upload.get_basename(image_path)
            return {"message": f"{basename} image has been successfully uploaded."}, 201
        except UploadNotAllowed:
            extension = image_upload.get_extension(data["image"])
            return {"message": f"{extension} is not valid."}, 400
        
class Image(Resource):
    def get(self, path):
        filename = image_upload.get_basename(path)
        folder = image_upload.get_path_without_basename(path)
        
        if not image_upload.is_filename_safe(filename):
            return {"message": "Not a valid file."}, 400
        
        try:
            return send_file(image_upload.get_path(filenmae=filename, folder=folder))
        except FileNotFoundError:
            return {"message": "File does not exist."}, 404
        
    def delete(self, path):
        filename = image_upload.get_basename(path)
        folder = image_upload.get_path_without_basename(path)
        
        if not image_upload.is_filename_safe(filename):
            return {"message": "Not a valid file name."}, 400
        
        try:
            os.remove(image_upload.get_path(filename, folder=folder))
            return {"message": "Image has been deleted."}, 200
        except FileNotFoundError:
            return {"message": "Image cannot be found."}, 404
        except:
            traceback.print_exc()
            return {"message": "Failed to delete file. Try again later."}, 500