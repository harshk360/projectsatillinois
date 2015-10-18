from flask import redirect, request, session, url_for
from flask.ext import admin
from models import User
from sqlalchemy import func
from app_and_db import db
import flask_admin.contrib.sqla

class MyAdminView(admin.AdminIndexView):
  def is_accessible(self):
    try:
      user = User.query.filter_by(id=session['id']).first()
      return user.is_admin
    except:
      return False

  def _handle_view(self, name, **kwargs):
    if not self.is_accessible():
      return redirect(url_for('index', next=request.url))

  @admin.expose('/')
  def index(self):
    users = db.session.query(func.count(User.id)).scalar()
    return self.render('admin/index.html', users = users)

class ModelViewAuth(flask_admin.contrib.sqla.ModelView):
  def is_accessible(self):
    try:
      user = User.query.filter_by(id=session['id']).first()
      return user.is_admin
    except:
      return False
