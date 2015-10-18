from flask import redirect, request, session, url_for
from flask.ext import admin
from models import User, Project, Visit, Comment
from sqlalchemy import func
from app_and_db import db
import datetime
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
    projects = db.session.query(func.count(Project.id)).scalar()
    current_time = datetime.datetime.utcnow()
    one_week_ago = current_time - datetime.timedelta(weeks=1)
    visits = db.session.query(Visit).filter(Visit.timestamp.between(one_week_ago, current_time)).count()
    comments = db.session.query(Comment).filter(Comment.timestamp.between(one_week_ago, current_time)).count()
    return self.render('admin/index.html', users = users, projects = projects, visits = visits, comments = comments)

class ModelViewAuth(flask_admin.contrib.sqla.ModelView):
  def is_accessible(self):
    try:
      user = User.query.filter_by(id=session['id']).first()
      return user.is_admin
    except:
      return False
