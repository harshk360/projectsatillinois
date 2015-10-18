from models import Skill
from app_and_db import app, db
from startup import init_app

init_app(app, db)

skills = {
  'Android' : 'Mobile',
  'iOS' : 'Mobile',
  'Windows Phone' : 'Mobile',
  'Phone Gap' : 'Mobile',
  'Cordova' : 'Mobile',
  'Objective-C' : 'Mobile',
  'Swift' : 'Mobile',
  
  'SQL' : 'Databases',
  'MySQL' : 'Databases',
  'PostgreSQL' : 'Databases',

  'Javascript' : 'Web Development',
  'JQuery' : 'Web Development',
  'Bootstrap' : 'Web Development',
  'AngularJS' : 'Web Development',
  'React' : 'Web Development',
  'Flask' : 'Web Development',
  'HTML' : 'Web Development',
  'CSS' : 'Web Development',
  'CSS3' : 'Web Development',

  'Python' : 'Programming Languages',
  'Java' : 'Programming Languages',
  'C++' : 'Programming Languages',
  'C' : 'Programming Languages',
  'PHP' : 'Programming Languages',
  'C#' : 'Programming Languages'
}


for key, value in skills.items():
  skill = Skill(key, value)
  db.session.add(skill)
db.session.commit()