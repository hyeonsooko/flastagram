from ..db import db
from sqlalchemy.sql import func

class PostModel(db.Model):
    
    __tablename__ = "Post"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    author = db.relationship("UserModel", backref="post_author")
    comment_set = db.relationship("CommentModel", backref="post", passive_deletes=True)
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f"<Post Object: {self.title}>"
    
    def update_to_db(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
    