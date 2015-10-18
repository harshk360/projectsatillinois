from flask import Flask
from flask import jsonify, redirect, render_template, request, session, url_for
from flask.ext import admin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
from config import BaseConfig
from math import ceil
from app_and_db import app, db
from models import User, Visit, Project

@app.before_request
def log_request():
  id = None
  if 'id' in session:
    id = session['id']
  if "favicon" in request.path or "static" in request.path or "admin" in request.path or "api" in request.path:
    return
  # TODO: check if url_rule is project   
  visit = Visit(id, None, None, request.remote_addr, request.path)
  db.session.add(visit)
  db.session.commit()

@app.route('/')
def index():
  return app.send_static_file("views/index.html")

@app.errorhandler(404)
def is404(e):
  return render_template('error.html', e = e)

@app.route('/api/v1/project', defaults={'page': 1})
@app.route('/api/v1/projects/', defaults={'page': 1})
@app.route('/api/v1/projects/page/<int:page>')
def get_events(page):
    number_per_page = 8
    start_index = ((page - 1) * number_per_page)
    projects = Project.query.order_by(asc(Project.id)).offset(start_index).limit(number_per_page)
    end_page = ceil(db.session.query(func.count(Project.id)).scalar() / float(number_per_page))

    return jsonify(projects=[project.serialize() for project in projects], page = page, number_of_pages = int(end_page))

@app.route('/api/user/current')
def get_current_user():
  if not ('logged_in' in session and session['logged_in']):
    return jsonify(error = "No user logged in"), 404
  try:
    user = User.query.filter_by(id=session['id']).first()
    return jsonify(user.serialize())
  except NoResultFound as e:
    return jsonify(error = "No user logged in"), 404

# @app.route('/api/user/current/update', methods=['POST'])
# def update_current_user():
#     if not ('logged_in' in session and session['logged_in']):
#         return jsonify(error = "No user logged in"), 404
#     try:
#         user = db.session.query(User).filter_by(id=session['id']).first()
#         user.academic_major = request.get_json()['academic_major']
#         user.graduation_year = request.get_json()['graduation_year']
#         db.session.commit()
#         return jsonify(user.serialize())
#     except NoResultFound as e:
#         return jsonify(error = "No user logged in"), 404


# @app.route('/api/user/<int:id>')
# def get_user_profile(id):
#     try:
#         user = User.query.filter(User.id == id).one()
#         return jsonify(user.serialize())
#     except NoResultFound as e:
#         return jsonify(error = "No user found for id " + str(id)), 404