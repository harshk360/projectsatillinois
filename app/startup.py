from config import BaseConfig
from admin import MyAdminView, ModelViewAuth
from flask.ext.admin import Admin
def init_app(app, db):
  #setup db credentials
  app.config.from_object(BaseConfig)

  #import routes
  import facebook_login
  import projects_routes

  #setup admin
  from models import *
  admin = Admin(app, index_view=MyAdminView())
  admin.add_view(ModelViewAuth(User, db.session, name="Users"))
  admin.add_view(ModelViewAuth(Project, db.session, name="Projects"))
  admin.add_view(ModelViewAuth(Login, db.session, name="Logins"))
  admin.add_view(ModelViewAuth(Visit, db.session, name="Visits"))
  admin.add_view(ModelViewAuth(User_Project, db.session, name="Users to Projects"))
  admin.add_view(ModelViewAuth(Image, db.session, name="Images"))
  admin.add_view(ModelViewAuth(Comment, db.session, name="Comments"))
  admin.add_view(ModelViewAuth(Skill, db.session, name="Skills"))
  admin.add_view(ModelViewAuth(User_Skill, db.session, name="Skills to Users"))
  admin.add_view(ModelViewAuth(Project_Skill, db.session, name="Skills to Projects"))