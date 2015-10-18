from sqlalchemy import ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func
from sqlalchemy.types import Enum
from flask.ext.sqlalchemy import SQLAlchemy 
from app_and_db import db
from datetime import datetime

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  github_auth = db.Column(db.String(255))
  fb_id = db.Column(db.String(255))
  avatar = db.Column(db.String(255))
  academic_major = db.Column(db.String(255))
  graduation_month = db.Column(mysql.INTEGER(2))
  graduation_year = db.Column(mysql.INTEGER(4))
  description = db.Column(mysql.MEDIUMTEXT())
  is_admin = db.Column(db.Boolean(), nullable=False, default=False)

  def __init__(self, full_name="", fb_id="", email=""):
    self.full_name = full_name
    self.fb_id = fb_id
    self.email = email
    self.avatar = "https://graph.facebook.com/{0}/picture?width=9999".format(fb_id)

  def __str__(self):
    return self.full_name

  def serialize(self):
    return {
        'id' : self.id,
        'full_name': self.full_name,
        'avatar' : self.avatar
    }

class Login(db.Model):
  __tablename__ = "logins"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  
  user = db.relationship("User")

  def __init__(self, user_id, timestamp = datetime.now()):
    self.user_id = user_id
    self.timestamp = timestamp 

class Visit(db.Model):
  __tablename__ = "visits"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=True)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  
  ip_address = db.Column(db.String(255), nullable = False)
  url = db.Column(db.String(255), nullable = False)
  user = db.relationship("User")
  project = db.relationship("Project")

  def __init__(self, user_id, project_id, timestamp, ip_address, url):
    self.user_id = user_id
    self.project_id = project_id
    self.timestamp = timestamp
    self.ip_address = ip_address
    self.url = url

class Project(db.Model):
  __tablename__ = "projects"
  enum = Enum('IN_PROGRESS','COMPLETED', 'DELETED')
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  status = db.Column(enum, nullable=False)
  cost = db.Column(db.DECIMAL(6, 2))
  youtube_url = db.Column(db.String(255))
  github_url = db.Column(db.String(255))
  description = db.Column(mysql.MEDIUMTEXT())
  owner_id = db.Column(db.Integer(), ForeignKey("users.id"))
  owner = db.relationship("User")
  images = db.relationship("Image")
  skills = db.relationship("Project_Skill")
  comments = db.relationship("Comment")

  def __str__(self):
    return self.name

  def serialize(self):
    return {
      'id' : self.id,
      'name' : self.name,
      'status' : self.status,
      # 'cost' : float(self.cost),
      'youtube_url' : self.youtube_url,
      'github_url' : self.github_url,
      'description' : self.description,
      'owner' : self.owner.serialize(),
      'images' : [image.serialize() for image in self.images],
      'skills' : [skill.serialize() for skill in self.skills],
      'comments' : [comment.serialize() for comment in self.comments]
    }

class User_Project(db.Model):
  __tablename__ = "user_projects"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  user = db.relationship("User")
  project = db.relationship("Project")

class Image(db.Model):
  __tablename__ = "images"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  url = db.Column(db.String(255))
  file_name = db.Column(db.String(255))
  image_name = db.Column(db.String(255), nullable=False)
  project = db.relationship("Project")

  def serialize(self):
    return {
      'url' : self.url,
      'image_name' : self.image_name
    }

class Comment(db.Model):
  __tablename__ = "comments"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  
  comment = db.Column(mysql.MEDIUMTEXT(), nullable=False)
  user = db.relationship("User")
  project = db.relationship("Project")

  def serialize(self):
    return {
      'comment' : self.comment,
      'user' : self.user.serialize()
    }

  def __str__(self):
    return self.comment

class Skill(db.Model):
  __tablename__ = "skills"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  type = db.Column(db.String(255), nullable=False)

  def __init__(self, name, type):
    self.name = name
    self.type = type

  def serialize(self):
    return {
      'name' : self.name,
      'type' : self.type
    }

  def __str__(self):
    return self.name

class User_Skill(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  skill_id = db.Column(db.Integer(), ForeignKey("skills.id"), nullable=False)
  user = db.relationship("User")
  skill = db.relationship("Skill")
  def serialize(self):
    return {
      'skill' : self.skill.serialize()
    }

class Project_Skill(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  skill_id = db.Column(db.Integer(), ForeignKey("skills.id"), nullable=False)
  skill = db.relationship("Skill")
  project = db.relationship("Project")

  def serialize(self):
    return {
      'skill' : self.skill.serialize()
    }