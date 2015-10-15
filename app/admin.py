from app import admin
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from models import *


class MyView(BaseView):
    def is_accessible(self):
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('index', next=request.url))

    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin.add_view(ModelView(User, db.session))
