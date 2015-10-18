from sqlalchemy import ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func
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

  def __repr__(self):
    return '<User {0} {1}>'.format(self.first_name, self.last_name)


  def serialize(self):
    return {
        'id' : self.id,
        'full_name': self.full_name,
        'avatar' : self.avatar
    }

class Login(db.Model):
  __tablename__ = "logins"
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  

  def __init__(self, user, timestamp = datetime.now()):
    self.user = user
    self.timestamp = timestamp 

class Visit(db.Model):
  __tablename__ = "visits"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=True)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  
  ip_address = db.Column(db.String(255), nullable = False)

class Project(db.Model):
  __tablename__ = "projects"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  status = db.Column(db.String(255), nullable=False)
  cost = db.Column(db.DECIMAL(6, 2))
  youtube_url = db.Column(db.String(255))
  github_url = db.Column(db.String(255))
  description = db.Column(mysql.MEDIUMTEXT())
  owner = db.Column(db.Integer(), ForeignKey("users.id"))

class User_Project(db.Model):
  __tablename__ = "user_projects"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)

class Image(db.Model):
  __tablename__ = "images"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  url = db.Column(db.String(255))
  file_name = db.Column(db.String(255))
  image_name = db.Column(db.String(255), nullable=False)

class Comment(db.Model):
  __tablename__ = "comments"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  
  comment = db.Column(mysql.MEDIUMTEXT(), nullable=False)

class Skill(db.Model):
  __tablename__ = "skills"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  type = db.Column(db.String(255), nullable=False)

  def __init__(self, name, type):
    self.name = name
    self.type = type

class User_Skill(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  skill_id = db.Column(db.Integer(), ForeignKey("skills.id"), nullable=False)

class Project_Skill(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  skill_id = db.Column(db.Integer(), ForeignKey("skills.id"), nullable=False)