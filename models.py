"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String,
                           nullable=False)
    
    last_name = db.Column(db.String,
                          nullable=False)
    
    image_url = db.Column(db.String,
                          nullable=True,
                          default='https://media.istockphoto.com/id/1495088043/vector/user-profile-icon-avatar-or-person-icon-profile-picture-portrait-symbol-default-portrait.jpg?s=612x612&w=0&k=20&c=dhV2p1JwmloBTOaGAtaA3AW1KSnjsdMt7-U_3EZElZ0=')
    
    posts = db.relationship("Post", backref="user")
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String,
                      nullable=False)
    
    content = db.Column(db.String,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    tags = db.relationship("Tag", secondary="posttags", backref="posts")
    
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String,
                     unique=True)
    

class PostTag(db.Model):
    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True,
                        )
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)