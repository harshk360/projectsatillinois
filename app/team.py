from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import mysql
from flask import jsonify
from sqlalchemy.orm import relationship
from team_signup import Team_Signup

class Team(db.Model):

    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255))
    event_id = db.Column(db.Integer(), ForeignKey("events.id"))
    submission_link = db.Column(db.String(255))
    privacy = db.Column(db.String(255), default="public")
    max_size = db.Column(db.Integer())
    description = db.Column(mysql.MEDIUMTEXT())

    def get_teammates(self):
        signups = Team_Signup.query.filter(Team_Signup.team_id == self.id).all()
        teammates = []
        for signup in signups:
            teammates.append(signup.user)
        return teammates

    def serialize(self):
        return {
            'id' : self.id,
            'team_name' : self.team_name,
            'event_id' : self.event_id,
            'submission_link' : self.submission_link,
            'privacy' : self.privacy,
            'max_size' : self.max_size,
            'teammates' : [teammate.serialize() for teammate in self.get_teammates()],
            'description' : self.description
        }