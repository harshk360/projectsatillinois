from sqlalchemy import ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func
from sqlalchemy.types import Enum
from flask.ext.sqlalchemy import SQLAlchemy 
from app_and_db import db
from datetime import datetime

class User_Skill(db.Model):
  __tablename__ = "user_skills"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  skill_id = db.Column(db.Integer(), ForeignKey("skills.id"), nullable=False)

  def serialize(self):
    return {
      'skill' : self.skill.serialize()
    }

  def __str__(self):
    return self.skill.__str__()

class Project_Skill(db.Model):
  __tablename__ = "project_skills"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  skill_id = db.Column(db.Integer(), ForeignKey("skills.id"), nullable=False)

  def serialize(self):
    return {
      'skill' : self.skill.serialize()
    }

  def __str__(self):
    return self.skill.__str__()

class User_Project(db.Model):
  __tablename__ = "user_projects"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  github_auth = db.Column(db.String(255))
  fb_id = db.Column(db.String(255))
  avatar = db.Column(db.String(255))
  major = Enum('Computer Science', 'Electical Engineering', 'Other')
  academic_major = db.Column(major)
  month = Enum('May','December')
  year = Enum('2015', '2016', '2017', '2018', '2019', '2020')
  graduation_month = db.Column(month)
  graduation_year = db.Column(year)
  description = db.Column(mysql.MEDIUMTEXT())
  is_admin = db.Column(db.Boolean(), nullable=True, default=False)

  skills = db.relationship("Skill", secondary="user_skills", backref="users")

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
        'avatar' : self.avatar,
        'graduation_month' : self.graduation_month,
        'graduation_year' : self.graduation_year,
        'description' : self.description,
        'academic_major' : self.academic_major,
        'skills' : [skill.serialize() for skill in self.skills]
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
  enum = Enum('In Progress','Completed', 'Deleted')
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  status = db.Column(enum, nullable=False)
  cost = db.Column(db.DECIMAL(6, 2))
  youtube_url = db.Column(db.String(255))
  github_url = db.Column(db.String(255))
  subtitle = db.Column(db.String(255))
  description = db.Column(mysql.MEDIUMTEXT())
  owner_id = db.Column(db.Integer(), ForeignKey("users.id"))
  owner = db.relationship("User", backref="projects")
  images = db.relationship("Image")
  skills = db.relationship("Skill", secondary="project_skills", backref="projects")
  team_members = db.relationship("User", secondary="team_members", backref="users")
  comments = db.relationship("Comment", backref="projects")

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
      'subtitle' : self.subtitle,
      'description' : self.description,
      'owner' : self.owner.serialize(),
      'images' : [image.serialize() for image in self.images],
      'skills' : [skill.serialize() for skill in self.skills],
      'comments' : [comment.serialize() for comment in self.comments],
      'team_members' : [member.serialize() for member in self.team_members]
    }

class Image(db.Model):
  __tablename__ = "images"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  url = db.Column(db.String(255))
  file_name = db.Column(db.String(255))
  subtitle = db.Column(db.String(255), nullable=False)

  def serialize(self):
    return {
      'id' : self.id,
      'url' : self.url,
      'subtitle' : self.subtitle
    }

  def __str__(self):
    return self.subtitle

class Comment(db.Model):
  __tablename__ = "comments"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
  timestamp = db.Column(db.TIMESTAMP(), default=func.now(), nullable=False)  
  comment = db.Column(mysql.MEDIUMTEXT(), nullable=False)
  user = db.relationship("User", backref="comments")

  def serialize(self):
    return {
      'comment' : self.comment,
      'user' : self.user.serialize(),
      'timestamp' : self.timestamp.isoformat()
    }

  def __str__(self):
    return self.comment

class Skill(db.Model):
  __tablename__ = "skills"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  type = db.Column(db.String(255), nullable=False)

  #Required for Admin
  def __init__(self):
    return

  def __init__(self, name, typeName):
    self.name = name
    self.type = type

  def serialize(self):
    return {
      'name' : self.name,
      'type' : self.type
    }

  def __str__(self):
    return self.name 

class Team_Member(db.Model):
  __tablename__ = "team_members"
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer(), ForeignKey("projects.id"), nullable=False)
  user_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)