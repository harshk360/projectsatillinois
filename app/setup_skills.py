from models import Skill
from app_and_db import app, db
from startup import init_app

init_app(app, db)

mobile = {
  'Android' : 'Mobile',
  'iOS' : 'Mobile',
  'Windows Phone' : 'Mobile',
  'Phone Gap' : 'Mobile',
  'Cordova' : 'Mobile',
  'Objective-C' : 'Mobile',
  'Swift' : 'Mobile'
  }
databases = {
  'SQL' : 'Databases',
  'MySQL' : 'Databases',
  'PostgreSQL' : 'Databases',
  'MongoDB' : 'Databases',
  'Firebase' : 'Databases',
  'Oracle' : 'Databases',
  'Microsoft SQL Server' : 'Databases'
  }

web_dev = {'Javascript' : 'Web Development',
  'JQuery' : 'Web Development',
  'Bootstrap' : 'Web Development',
  'AngularJS' : 'Web Development',
  'Ember' : 'Web Development',
  'BackboneJS' : 'Web Development',
  'React' : 'Web Development',
  'Polymer' : 'Web Development',
  'Ruby on Rails' : 'Web Development',
  'Flask' : 'Web Development',
  'Spring' : 'Web Development',
  'NodeJS' : 'Web Development',
  'Express' : 'Web Development',
  'HTML' : 'Web Development',
  'CSS' : 'Web Development'
  }

languages = {'Python' : 'Programming Languages',
  'Java' : 'Programming Languages',
  'C++' : 'Programming Languages',
  'C' : 'Programming Languages',
  'PHP' : 'Programming Languages',
  'C#' : 'Programming Languages',
  'Go' : 'Programming Languages',
  'Rust' : 'Programming Languages',
  'Scala' : 'Programming Languages'
}


for key, value in mobile.items():
  skill = Skill(key, value)
  db.session.add(skill)
db.session.commit()

for key, value in databases.items():
  skill = Skill(key, value)
  db.session.add(skill)
db.session.commit()

for key, value in web_dev.items():
  skill = Skill(key, value)
  db.session.add(skill)
db.session.commit()

for key, value in languages.items():
  skill = Skill(key, value)
  db.session.add(skill)
db.session.commit()