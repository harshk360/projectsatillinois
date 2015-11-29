from app_and_db import app, db
from flask import abort, jsonify, redirect, render_template, request, session, url_for
from math import ceil
from models import User, Project, Image, Comment, Team_Member
from sqlalchemy import asc
from sqlalchemy.sql import func
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.fields import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea, HiddenInput
from wtforms.validators import StopValidation, Required, ValidationError, InputRequired, URL, Email
from copy import deepcopy
from recommendation import search

import re
import requests

@app.route('/api/v1/project', defaults={'page': 1})
@app.route('/api/v1/projects/', defaults={'page': 1})
@app.route('/api/v1/projects/page/<int:page>')
def get_projects(page):
  number_per_page = 8
  start_index = ((page - 1) * number_per_page)
  projects = Project.query.filter(Project.status != "Deleted").order_by(asc(Project.id)).offset(start_index).limit(number_per_page)
  end_page = ceil(db.session.query(func.count(Project.id)).scalar() / float(number_per_page))
  return jsonify(projects=[project.serialize() for project in projects], page = page, number_of_pages = int(end_page))

@app.route('/api/v1/project/<string:status>', defaults={'page': 1})
@app.route('/api/v1/projects/<string:status>', defaults={'page': 1})
@app.route('/api/v1/projects/page/<int:page>/<string:status>')
def get_projects_by_status(page, status):
  if "in" in status.lower() and "progress" in status.lower():
    status = "In Progress"
  if "delete" in status.lower():
    status = "Deleted"
  if "complete" in status.lower():
    status = "Completed"
  number_per_page = 8
  start_index = ((page - 1) * number_per_page)
  projects = Project.query.filter(Project.status==status).order_by(asc(Project.id)).offset(start_index).limit(number_per_page)
  end_page = ceil(db.session.query(func.count(Project.id)).scalar() / float(number_per_page))
  return jsonify(projects=[project.serialize() for project in projects], page = page, number_of_pages = int(end_page))

@app.route('/api/v1/project/<int:id>')
def get_project_by_id(id):
  project = Project.query.filter_by(id=id).first()
  images = Image.query.filter_by(project_id=id).all()
  return jsonify(project = project.serialize(), images = [image.serialize() for image in images])

@app.route('/api/v1/project/<int:id>/<string:status>')
def update_project_status_by_id(id, status):
  project = Project.query.filter_by(id=id).first()
  status = status.upper()
  if status not in Project.status.property.columns[0].type.enums:
    return jsonify(error="Invalid status"), 400
  project.status = status
  try:
    db.session.add(project)
    db.session.commit()
    return jsonify(project=project.serialize())
  except e:
    return jsonify(error=str(e)), 500

@app.route('/project/edit/<int:id>', methods = ['GET', 'POST'])
def edit_project(id):
  MyForm = model_form(Project, base_class=Form, exclude_fk=True, db_session=db.session, field_args={
    'name' : {'validators' : [InputRequired()]},
    'description': {'widget': TextArea()},
    'youtube_url': {'validators': [valid_youtube_link]},
    'github_url': {'validators': [valid_github_link]}
  })
  project = db.session.query(Project).filter_by(id=id).first()
  if project is None or project.owner_id != session['id']:
    abort(404)
  form = MyForm(request.form, project)
  if form.validate_on_submit():
    update_fields(project, form)
    return render_template("create_project.html", form=form, success=True, url = "/project/edit/" + str(id))
  return render_template("create_project.html", form=form, url = "/project/edit/" + str(id))

@app.route('/project/add', methods = ['GET', 'POST'])
def create_new_project():
  MyForm = model_form(Project, base_class=Form, db_session=db.session, field_args={
    'name' : {'validators' : [InputRequired()]},
    'description': {'widget': TextArea()},
    'youtube_url': {'validators': [valid_youtube_link]},
    'github_url': {'validators': [valid_github_link]},
    'cost' : {'description' : "You can provide a reward for helping with a project"}
  })
  project = Project()
  form = MyForm(request.form, project)
  if form.validate_on_submit():
    project.owner_id = session['id']
    update_fields(project, form)
    return "/project/" + str(project.id), 201
  return render_template("create_project.html", form=form, url = "/project/add")

def update_fields(project, form):
  project.name = form.name.data
  project.subtitle = form.subtitle.data
  project.status = form.status.data
  project.cost = form.cost.data
  project.youtube_url = form.youtube_url.data
  project.github_url = form.github_url.data
  project.description = form.description.data
  project.skills = form.skills.data
  db.session.add(project)
  db.session.commit()

def valid_youtube_link(form, field):
  if form.youtube_url.data is not None and len(form.youtube_url.data) > 0:
    youtube_regex = (
    r'(https?://)?(www\.)?'
    '(youtube|youtu|youtube-nocookie)\.(com|be)/'
    '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, form.youtube_url.data)
    if youtube_regex_match:
      return
    raise ValidationError('Invalid YouTube Link')

def valid_github_link(form, field):
  if form.github_url.data is not None and len(form.github_url.data) > 0:
    if not form.github_url.data.startswith("https://github.com"):
      raise ValidationError('Github link must start with https://www.github.com')

@app.route('/project/add/<int:id>/image', methods = ['GET', 'POST'])
def attach_image_to_project(id):
  MyForm = model_form(Image, base_class=Form, exclude_fk = True, db_session=db.session, field_args={
    'subtitle': {'validators' : [InputRequired()]},
    'url': {'validators': [InputRequired(), URL(), valid_image_link]}}
    )
  image = Image(project_id = id)
  form = MyForm(request.form, image)
  if form.validate_on_submit():
    image.subtitle = form.subtitle.data
    image.url = form.url.data
    db.session.add(image)
    db.session.commit()
    return "success", 201
  return render_template("create_image.html", form=form, url = "/project/add/" + str(id) + "/image")

def valid_image_link(form, field):
  url = form.url.data
  if url is not None and len(url) > 0:
    if not (url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".gif")):
      raise ValidationError("Not a valid image format (should be JPEG or PNG or GIF)")
    if requests.get(url).status_code is not 200:
      raise ValidationError("Image is invalid link")

@app.route('/api/v1/delete/image/<int:id>')
def delete_image(id):
  image = db.session.query(Image).filter_by(id=id).first()
  db.session.delete(image)
  db.session.commit()
  return jsonify(success="deleted")

@app.route('/project/add/<int:id>/team_member', methods = ['GET', 'POST'])
def attach_team_member_to_project(id):
  form = EmailForm()
  if form.validate_on_submit():
    user = db.session.query(User).filter_by(email=form.email.data).first()
    team_member = Team_Member()
    team_member.project_id = id
    team_member.user_id = user.id
    db.session.add(team_member)
    db.session.commit()
    return "success", 201
  return render_template("create_team_member.html", form=form, url = "/project/add/" + str(id) + "/team_member")

@app.route('/api/v1/delete/team_member/<int:project_id>/<int:user_id>')
def delete_team_member(project_id, user_id):
  team_member = db.session.query(Team_Member).filter_by(project_id=project_id, user_id=user_id).first()
  db.session.delete(team_member)
  db.session.commit()
  return jsonify(success="deleted")

def valid_user(form, field):
  email = form.email.data
  try:
    user = db.session.query(User).filter_by(email=email).first()
    if user is None:
      raise ValidationError("Invalid User")
  except Exception as e:
    raise ValidationError("Invalid User")

class EmailForm(Form):
    email = EmailField('Email address', [InputRequired(), Email(), valid_user])

@app.route('/project/add/<int:id>/comment', methods = ['GET', 'POST'])
def attach_comment_to_project(id):
  form = CommentForm()
  if form.validate_on_submit():
    comment = Comment()
    comment.user_id = session['id']
    comment.project_id = id
    comment.comment = form.comment.data
    db.session.add(comment)
    db.session.commit()
    return "success", 201
  return render_template("create_comment.html", form=form, url = "/project/add/" + str(id) + "/comment")


@app.route('/recommend', methods = ['GET'])
def recommend_projects():
    user = User.query.filter_by(id=session['id']).first()
    projects = Project.query.filter(Project.status=="In Progress").all()
    scoreList = recommendation.search(user, projects)
    return jsonify(scoreList)

class CommentForm(Form):
    comment = TextAreaField('Comment', [InputRequired()])
