from flask import Flask
from flask import jsonify, redirect, render_template, request, session, url_for
from flask.ext import admin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from app_and_db import app, db
from models import User, Visit, Project

@app.before_request
def log_request():
  id = None
  project_id = None
  if 'id' in session:
    id = session['id']
  if "favicon" in request.path or "static" in request.path or "admin" in request.path:
    return
  if "/api/v1/project/<int:id>" in str(request.url_rule):
    project_id = request.path[request.path.rfind('/') + 1:]
  try:
    visit = Visit(id, project_id, None, request.remote_addr, request.path)
    db.session.add(visit)
    db.session.commit()
  except:
    db.session.rollback()

@app.route('/')
def index():
  return app.send_static_file("views/index.html")

@app.errorhandler(404)
def is404(e):
  return render_template('error.html', e = e)

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