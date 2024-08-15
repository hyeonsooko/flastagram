from ..db import db

followers = db.Table(
        'followers',
        # 내가 팔로우하는 사람들의 id 
        db.Column('follower_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True),
        # 내가 팔로우한 사람들의 id
        db.Column('followed_id', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    )

class UserModel(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    followed = db.relationship(
        'UserModel',
        secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('follower_set', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
        
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f'<User Object : {self.username}>'
    
class RefreshTokenModel(db.Model):
    __tablename__ = "RefreshToken"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("UserModel", backref="token")
    refresh_token_value = db.Column(db.String(512), nullable=False, unique=True)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_user_by_token(cls, token):
        
        try:
            user_id = cls.query.filter_by(refresh_token_value=token).first().user_id
        except AttributeError:
            return None
        user = UserModel.find_by_id(id=user_id)
        return user