import json
import logging
from conf import settings
from flask import request
from flask.views import MethodView
from myapp.common.Response import response
from myapp.model.users import User
from myapp.database import db_session
# from sqlalchemy.sql import select


class Register(MethodView):
    log = logging.getLogger('Register')

    def post(self):
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter(User.email==post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # insert the user
                db_session.add(user)
                db_session.commit()
                # generate the auth token
                # auth_token = user.encode_auth_token(user.id, settings.login_expire_sec)
                auth_token = user.encode_auth_token(user.id)
                self.log.info(auth_token)
                content = {'auth_token': auth_token}
                return response(201, 0, content=content)
            except Exception as e:
                self.log.info(str(e))
                return response(401, 101)
        else:
            return response(202, 102)


class Login(MethodView):
    log = logging.getLogger('Login')

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter(User.email==post_data.get('email')).first()
            if user:
                if user.check_password(post_data.get('password')):
                    auth_token = user.encode_auth_token(user.id, )
                    if auth_token:
                        content = {'auth_token': auth_token}
                        return response(200, 0, content=content)
                else:
                    return response(202, 103)
            else:
                return response(202, 103)
        except Exception as e:
            self.log.info(str(e))
            return response(500, 1)


class Logout(MethodView):
    log = logging.getLogger('Logout')

    def post(self):
        try:
            # fetch the user data
            token = request.headers.get('Authorization')
            if token:
                return response(200, 0)
        except Exception as e:
            self.log.info(str(e))
            return response(500, 1)
    