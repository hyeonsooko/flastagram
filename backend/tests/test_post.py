import email
import os
from urllib import response

import sys
sys.path.insert(0, 'C:\\code\\projects\\flastagram\\backend')
import api
import unittest
from api.db import db
from dotenv import load_dotenv
from api.models.post import PostModel
from api.models.user import UserModel
from sqlalchemy.orm import Session
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class CommonTestCaseSettings(unittest.TestCase):
    
    def setUp(self):
        """
        testing setup
        using backend/config/test.py
        using environment from APPLICATION_SETTINGS_FOR_TEST in .env file
        client created using app.test_client()
        creating a user for testing
        """
        self.app = api.create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        load_dotenv(".env", verbose=True)
        self.app.config.from_object("config.test")
        self.app.config.from_envvar("APPLICATION_SETTINGS_FOR_TEST")
        self.app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
        self.client = self.app.test_client()
        db.create_all()
        UserModel(username="test_user", password="1234", email="test@example.com").save_to_db()
        
    def tearDown(self):
        """
        method after testing, self desturction, db clear
        """
        db.session.remove()
        db.drop_all()
        
class PostListTestCase(CommonTestCaseSettings):
    """
    /posts , GET, POST testing
    GET /posts => list of all posts
    POST /posts => create a post
    """
    def test_get_post_list(self):
        """
        1. make 100 posts, /posts signal
        2. posts will look like (title="1 post", content="1 content")
        3. /posts should show all posts
        4. list of posts should show in 10s, pagination in reverse pk
        5. thus, first post's id should be 100
        6. first page of last post's id should be 91
        """
        
        # make 100 posts
        dummy_posts = []
        for i in range(100):
            dummy_posts.append(
                PostModel(
                    title=f"{i+1} post", content=f"{i+1} content", author_id = 1
                )
            )
        db.session.bulk_save_objects(dummy_posts)
        db.session.commit()
        
        # req to first page of posts
        response = self.client.get("https://127.0.0.1:5000/posts/").get_json()
        
        # first post of first page's id should be 100
        self.assertEqual(100, response[0]["id"])
        
        # last post of first page's id should be 91
        self.assertEqual(91, response[-1]["id"])
        
        # second page of posts
        response = self.client.get("https://127.0.0.1:5000/posts/?page=2").get_json()
        
        # first post of second page's id should be 90
        self.assertEqual(90, response[0]["id"])
        
        # last post of second page's id should be 81
        self.assertEqual(81, response[-1]["id"])
        
if __name__ == "__main__":
    unittest.main()