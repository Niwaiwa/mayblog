import os
# import tempfile

import pytest

# from flaskr import flaskr
# from flask import Flask
from flask.testing import FlaskClient
from app import app, init_db
from myapp.model.users import User
from myapp.database import db_session


@pytest.fixture
def client():
    """ init no auth client """
    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # os.close(db_fd)
    # os.unlink(app.config['DATABASE'])


# class CustomClient(FlaskClient):
#     def __init__(self, *args, **kwargs):
#         self.token = kwargs.pop("authentication")
#         super(CustomClient,self).__init__( *args, **kwargs)


@pytest.fixture
def seclient():
    """ init auth client """
    def get_user_token():
        user = db_session.query(User).filter(User.email=='testclient@gmail.com').first()
        if not user:
            user = User(
                email='testclient@gmail.com',
                password='testclient'
            )
            db_session.add(user)
            db_session.commit()
        auth_token = user.encode_auth_token(user.id)
        return auth_token

    token = get_user_token()
    client = app.test_client()
    # client.token = token
    client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
    # client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
    with client:
        yield client


# @pytest.fixture(scope='session')
# def seclient(test_registration):
#     """ init auth client """
    
#     app.config['TESTING'] = True

#     with app.test_client(authentication=test_registration) as client:
#         # with app.app_context():
#         #     init_db()
#         yield client
