from POSTCRUD import db,login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as serializer

@login_manager.user_loader
def login(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(10),nullable=True,unique=True)
    email=db.Column(db.String(120),nullable=True,unique=True)
    image_file=db.Column(db.String(20),nullable=False,default="default.jpeg")
    password=db.Column(db.String(60),nullable=True)
    posts=db.relationship("Post",backref="author",lazy=True)
    
    def get_reset_token(self,expires_sec=1800):
        s=serializer(current_app.config["SECRET_KEY"])
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token,expires_sec=1800):
        s=serializer(current_app.config["SECRET_KEY"])
        try:
            user_id=s.loads(token,max_age=expires_sec)['user_id']
        except Exception:
            return None
        return  User.query.get(user_id)        



    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"
        

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(15),nullable=True)
    date_posted=db.Column(db.DateTime,nullable=True,default=(datetime.utcnow))
    content=db.Column(db.String(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)


    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}','{self.content}',{self.user_id})"
