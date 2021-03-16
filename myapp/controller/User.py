import json
import logging
from flask import request, g
from flask.views import MethodView
from myapp.common.Response import response
from myapp.model.users import User
from myapp.database import db_session
# from sqlalchemy.sql import select


class UserAPI(MethodView):
    log = logging.getLogger('UserAPI')
    def get(self):
        self.log.info('UserAPI get')
        user = User.query.filter(User.id==g.user_id).first()
        content = {
            'user_id': user.id,
            'email': user.email,
            'admin': user.admin,
            'registered_on': user.registered_on
        }
        return response(200, 0, content=content)
