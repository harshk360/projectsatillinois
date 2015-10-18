from app_and_db import app, db
from flask import jsonify, redirect, render_template, request, session, url_for
from math import ceil
from models import Project, Image, Comment
from sqlalchemy import asc
from sqlalchemy.sql import func
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

@app.route('/api/v1/project', defaults={'page': 1})
@app.route('/api/v1/projects/', defaults={'page': 1})
@app.route('/api/v1/projects/page/<int:page>')
def get_projects(page):
  number_per_page = 8
  start_index = ((page - 1) * number_per_page)
  projects = Project.query.filter(Project.status!="DELETED").order_by(asc(Project.id)).offset(start_index).limit(number_per_page)
  end_page = ceil(db.session.query(func.count(Project.id)).scalar() / float(number_per_page))
  return jsonify(projects=[project.serialize() for project in projects], page = page, number_of_pages = int(end_page))

@app.route('/api/v1/project/<string:status>', defaults={'page': 1})
@app.route('/api/v1/projects/<string:status>', defaults={'page': 1})
@app.route('/api/v1/projects/page/<int:page>/<string:status>')
def get_projects_by_status(page, status):
  status = status.upper()
  number_per_page = 8
  start_index = ((page - 1) * number_per_page)
  projects = Project.query.filter(Project.status==status).order_by(asc(Project.id)).offset(start_index).limit(number_per_page)
  end_page = ceil(db.session.query(func.count(Project.id)).scalar() / float(number_per_page))
  return jsonify(projects=[project.serialize() for project in projects], page = page, number_of_pages = int(end_page))

@app.route('/api/v1/project/<int:id>')
def get_project_by_id(id):
  project = Project.query.filter_by(id=id).first()
  images = Image.query.filter_by(project_id=id).all()
  comments = Comment.query.filter_by(project_id=id).order_by(asc(Comment.timestamp)).all()
  return jsonify(project = project.serialize(), images = [image.serialize() for image in images], comments = [comment.serialize() for comment in comments])

@app.route('/api/v1/project/<int:id>/<string:status>')
def update_project_status_by_id(id, status):
  if id != session['id']:
    return jsonify(error="User does not own project"), 403
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