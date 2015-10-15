from flask import Flask
from flask import jsonify, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_oauth import OAuth
from sqlalchemy import asc
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
from config import BaseConfig
from math import ceil

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
admin = Admin(app)

#from models import *
from admin import *

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
        person = User(first_name, last_name, user_id, email)
        db.session.add(person)
        db.session.commit()
    session['id'] = User.query.filter_by(fb_id=user_id).first().id

    return redirect(next_url)

@app.route('/logout')
def logout():
    pop_login_session()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return app.send_static_file("views/index.html")

@app.route('/api/project', defaults={'page': 1})
@app.route('/api/projects/', defaults={'page': 1})
@app.route('/api/projects/page/<int:page>')
def get_events(page):
    number_per_page = 8
    start_index = ((page - 1) * number_per_page)
    projects = Project.query.filter(Project.end_date >= func.now()).order_by(asc(Event.start_date)).offset(start_index).limit(number_per_page)
    end_page = ceil(Project.query.filter(Project.end_date >= func.now()).count() / float(number_per_page))

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

@app.route('/api/user/current/update', methods=['POST'])
def update_current_user():
    if not ('logged_in' in session and session['logged_in']):
        return jsonify(error = "No user logged in"), 404
    try:
        user = db.session.query(User).filter_by(id=session['id']).first()
        user.academic_major = request.get_json()['academic_major']
        user.graduation_year = request.get_json()['graduation_year']
        db.session.commit()
        return jsonify(user.serialize())
    except NoResultFound as e:
        return jsonify(error = "No user logged in"), 404


@app.route('/api/user/<int:id>')
def get_user_profile(id):
    try:
        user = User.query.filter(User.id == id).one()
        return jsonify(user.serialize())
    except NoResultFound as e:
        return jsonify(error = "No user found for id " + str(id)), 404

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"])
