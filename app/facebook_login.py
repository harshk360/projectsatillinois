from app import index
from app_and_db import app, db
from flask_oauth import OAuth
from flask import jsonify, redirect, render_template, request, session, url_for
from models import User, Login

oauth = OAuth()

facebook = oauth.remote_app('facebook',
  base_url='https://graph.facebook.com/',
  request_token_url=None,
  access_token_url='/oauth/access_token',
  authorize_url='https://www.facebook.com/dialog/oauth',
  consumer_key=app.config['FACEBOOK_APP_ID'],
  consumer_secret=app.config['FACEBOOK_APP_SECRET'],
  request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
  return session.get('facebook_token')

def pop_login_session():
  session.pop('logged_in', None)
  session.pop('facebook_token', None)

@app.route('/facebook_login')
def facebook_login():
  return facebook.authorize(callback=url_for('facebook_authorized',
    next=request.args.get('next'), _external=True))

@app.route('/facebook_authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
  next_url = request.args.get('next') or url_for('index')
  if resp is None or 'access_token' not in resp:
    return redirect(next_url)

  session['logged_in'] = True
  session['facebook_token'] = (resp['access_token'], '')
  data = facebook.get('/me').data
  user_id = data['id']
  first_name = data['first_name']
  last_name = data['last_name']
  email = data['email']
  if User.query.filter_by(fb_id=user_id).first() is None:
    person = User(first_name + " " + last_name, user_id, email)
    db.session.add(person)
    db.session.commit()
  id = User.query.filter_by(fb_id=user_id).first().id
  session['id'] = id
  login_audit = Login(id)
  db.session.add(login_audit)
  db.session.commit()
  return redirect(next_url)

@app.route('/logout')
def logout():
  pop_login_session()
  return redirect(url_for('index'))