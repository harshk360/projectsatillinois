from app import db
from sqlalchemy.dialects import mysql

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    picture_url = db.Column(db.String(255))
    fb_id = db.Column(db.String(255))
    email = db.Column(db.String(255))
    academic_major = db.Column(db.String(255))
    graduation_month = db.Column(mysql.INTEGER(2))
    graduation_year = db.Column(mysql.INTEGER(4))

    def __init__(self, first_name="", last_name="", fb_id="", email=""):
        self.first_name = first_name
        self.last_name = last_name
        self.fb_id = fb_id
        self.email = email
        self.picture_url = "https://graph.facebook.com/{0}/picture?width=9999".format(fb_id)


    def __repr__(self):
        return '<User {0} {1}>'.format(self.first_name, self.last_name)


    def serialize(self):
        return {
            'id' : self.id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'picture_url' : self.picture_url,
            'academic_major' : self.academic_major,
            'graduation_month' : self.graduation_month,
            'graduation_year' : self.graduation_year
        }
