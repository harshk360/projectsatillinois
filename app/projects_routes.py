from app_and_db import app, db
from flask import jsonify, redirect, render_template, request, session, url_for
from math import ceil
from models import Project, Image
from sqlalchemy import asc
from sqlalchemy.sql import func

@app.route('/api/v1/project', defaults={'page': 1})
@app.route('/api/v1/projects/', defaults={'page': 1})
@app.route('/api/v1/projects/page/<int:page>')
def get_projects(page):
    number_per_page = 8
    start_index = ((page - 1) * number_per_page)
    projects = Project.query.order_by(asc(Project.id)).offset(start_index).limit(number_per_page)
    end_page = ceil(db.session.query(func.count(Project.id)).scalar() / float(number_per_page))
    return jsonify(projects=[project.serialize() for project in projects], page = page, number_of_pages = int(end_page))

@app.route('/api/v1/project/<int:id>')
def get_project_by_id(id):
  project = Project.query.filter_by(id=id).first()
  images = Image.query.filter_by(project_id=id).all()
  return jsonify(project = project.serialize(), images = [image.serialize() for image in images])