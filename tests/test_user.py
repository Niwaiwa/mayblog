import json
import unittest
# from pytest import TestCase
from tests.client import client
from myapp.model.users import User
from myapp.database import db_session


class TestUserModel:
    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db_session.add(user)
        db_session.commit()
        auth_token = user.encode_auth_token(user.id)
        assert isinstance(auth_token, str)

    def test_decode_auth_token(self):
        user = User(
            email='test1@test.com',
            password='test1'
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        auth_token = user.encode_auth_token(user.id)
        assert isinstance(auth_token, str)
        assert User.decode_auth_token(auth_token) == user.id

class TestUser:
    def test_user_status(self, client):
        register_res = client.post(
            '/auth/register',
            json={
                'email': 'joess@gmail.com',
                'password': '123456'
            }
        )
        data = json.loads(register_res.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content']['auth_token']
        assert register_res.status_code == 201
        assert register_res.content_type == 'application/json'
        response = client.get(
            '/api/user/profile',
            headers={
                'Authorization': f'Bearer {data["content"]["auth_token"]}',
                'Content-Type': 'application/json'
            },
            # content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content'] is not None
        assert data['content']['email'] == 'joess@gmail.com'
        assert data['content']['admin'] is 'true' or 'false'
        assert response.status_code == 200
        assert response.content_type == 'application/json'