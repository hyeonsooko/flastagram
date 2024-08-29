from ..db import db
from sqlalchemy.sql import func
from sqlalchemy import or_

post_to_liker = db.Table(
    "post_liker",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("User.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "post_id",
        db.Integer,
        db.ForeignKey("Post.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

class PostModel(db.Model):
    
    __tablename__ = "Post"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    author = db.relationship("UserModel", backref="post_set")
    comment_set = db.relationship("CommentModel", backref="post", passive_deletes=True, lazy="dynamic")
    
    image = db.Column(db.String(255))
    
    liker = db.relationship(
        "UserModel",
        secondary=post_to_liker,
        backref=db.backref("post_liker_set", lazy="dynamic"),
        lazy="dynamic",
    )
    
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
        
    def do_like(self, user):
        if not self.is_like(user):
            self.liker.append(user)
            db.session.commit()
            return self
        
    def cancel_like(self, user):
        if self.is_like(user):
            self.liker.remove(user)
            db.session.commit()
            return self
        
    def is_like(self, user):
        return (
            self.liker.filter(post_to_liker.c.user_id == user.id).count() > 0
        )
    
    def get_liker_count(self):
        return self.liker.count()
    
    @classmethod
    def filter_by_followed(cls, followed_users):
        from api.models.user import UserModel
        
        if followed_users:
            return cls.query.filter(
                or_(cls.author == user for user in followed_users)
            ).order_by(PostModel.id.dsec())
        return UserModel.query.filter(False)