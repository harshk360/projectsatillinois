from app_and_db import app, db
from flask import jsonify, redirect, render_template, request, session, url_for
from models import User
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import validators
from wtforms.fields import SelectField, TextAreaField

class UpdateUserForm(Form):
  graduation_months = User.graduation_month.property.columns[0].type.enums
  graduation_years = User.graduation_year.property.columns[0].type.enums
  majors = User.academic_major.property.columns[0].type.enums

  academic_major = SelectField('Major', choices=[(g, g) for g in majors])
  graduation_month = SelectField('Graduation Month', choices=[(g, g) for g in graduation_months])
  graduation_year = SelectField('Graduation Year', choices=[(g, g) for g in graduation_years])
  description = TextAreaField("Tell us about yourself", [validators.optional(), validators.length(max=500)])

@app.route('/user/update', methods = ['GET', 'POST'])
def update_current_user():
  MyForm = model_form(User, base_class=Form, exclude_fk=True, db_session=db.session)
  user = db.session.query(User).filter_by(id=session['id']).first()
  form = MyForm(request.form, user)
  if form.validate_on_submit():
    user.academic_major = form.academic_major.data
    user.graduation_month = form.graduation_month.data
    user.graduation_year = form.graduation_year.data
    user.skills = form.skills.data
    user.description = form.description.data
    db.session.add(user)
    db.session.commit()
    return render_template("create_user.html", form=form, success=True, url=url_for('update_current_user'))
  for field, errors in form.errors.items():
    for error in errors:
      print field + " " + error
  return render_template("create_user.html", form=form, url=url_for('update_current_user'))

@app.route('/api/user/<int:id>')
def get_user_profile(id):
  try:
    user = User.query.filter(User.id == id).one()
    return jsonify(user.serialize())
  except NoResultFound as e:
    return jsonify(error = "No user found for id " + str(id)), 404