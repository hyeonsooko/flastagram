from ..db import db
from sqlalchemy.sql import func

class CommentModel(db.Model):
    
    __tablename__ = "Comment"
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
    author = db.relationship("UserModel", backref="comment_author")
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id', ondelete='CASCADE'), nullable=False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.sesison.commit()
        
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def __repr__(self):
        return f'<Comment Object : {self.content}>'