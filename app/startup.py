from config import BaseConfig
from admin import MyAdminView, ModelViewAuth
from flask.ext.admin import Admin
def init_app(app, db):
  #setup db credentials
  app.config.from_object(BaseConfig)

  #import views
  import facebook_login

  #setup admin
  from models import *
  admin = Admin(app, index_view=MyAdminView())
  admin.add_view(ModelViewAuth(User, db.session, name="Users"))