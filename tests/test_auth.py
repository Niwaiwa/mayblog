import json
import time
# from flask.globals import session
import pytest
import unittest
# from pytest import TestCase
from pytest import Cache
from tests.client import client


# class TestRegister(unittest.TestCase):
class TestRegister:

    # client = client()
    # def __init__(self, client):
        # super().__init__(methodName)
        # self.client = client
    # @pytest.fixture
    def test_registration(self, client, request):
        """ Test for user registration """
        # with client:
        response = client.post(
            '/auth/register',
            json={
                'email': 'joe@gmail.com',
                'password': '123456'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content']['auth_token']
        assert response.status_code == 201
        assert response.content_type == 'application/json'
        # return data['content']['auth_token']
        # request.config.cache.set('main/test', data['content']['auth_token'])
        # self.assertTrue(data['status'] == 0)
        # self.assertTrue(data['message'] == 'Successfully registered.')
        # self.assertTrue(data['auth_token'])
        # self.assertTrue(response.content_type == 'application/json')
        # self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self, client):
        """ Test for user registration with already registered user """
        response = client.post(
            '/auth/register',
            json={
                'email': 'joeal@gmail.com',
                'password': '123456'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content']['auth_token']
        assert response.status_code == 201
        assert response.content_type == 'application/json'
        response = client.post(
            '/auth/register',
            json={
                'email': 'joeal@gmail.com',
                'password': '123456'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 102
        assert data['msg'] == 'User already exists. Please Log in.'
        assert response.status_code == 202
        assert response.content_type == 'application/json'

    def test_registered_user_login(self, client):
        """ Test for login of registered-user login """
        # user registration
        resp_register = client.post(
            '/auth/register',
            json={
                'email': 'joes@gmail.com',
                'password': '123456',
            }
        )
        data_register = json.loads(resp_register.data)
        assert data_register['code'] == 0
        assert data_register['msg'] == 'ok'
        assert data_register['content']['auth_token']
        assert resp_register.content_type == 'application/json'
        assert resp_register.status_code == 201
        # registered user login
        response = client.post(
            '/auth/login',
            json={
                'email': 'joes@gmail.com',
                'password': '123456',
            }
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content']['auth_token']
        assert response.content_type == 'application/json'
        assert response.status_code == 200

    def test_not_registered_user_login(self, client):
        """ Test not registered user login """
        response = client.post(
            '/auth/login',
            json={
                'email': 'test_@gmail.com',
                'password': '123450'
            }
        )
        data = json.loads(response.data)
        assert data['code'] == 103
        assert data['msg'] == 'Log in failed, Please try again.'
        assert response.content_type == 'application/json'
        assert response.status_code == 202

    def test_valid_logout(self, client):
        resp_register = client.post(
            '/auth/register',
            json={
                'email': 'joesss@gmail.com',
                'password': '123456',
            }
        )
        data_register = json.loads(resp_register.data)
        assert data_register['code'] == 0
        assert data_register['msg'] == 'ok'
        assert data_register['content']['auth_token']
        assert resp_register.content_type == 'application/json'
        assert resp_register.status_code == 201
        # registered user login
        resp_login = client.post(
            '/auth/login',
            json={
                'email': 'joesss@gmail.com',
                'password': '123456',
            },
        )
        data = json.loads(resp_login.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content']['auth_token']
        assert resp_login.content_type == 'application/json'
        assert resp_login.status_code == 200
        response = client.post(
            '/auth/logout',
            headers={
                'Authorization': f'Bearer {data["content"]["auth_token"]}'
            },
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert response.content_type == 'application/json'
        assert response.status_code == 200

    def test_invalid_logout(self, client):
        resp_register = client.post(
            '/auth/register',
            json={
                'email': 'joesssd@gmail.com',
                'password': '123456',
            }
        )
        data_register = json.loads(resp_register.data)
        assert data_register['code'] == 0
        assert data_register['msg'] == 'ok'
        assert data_register['content']['auth_token']
        assert resp_register.content_type == 'application/json'
        assert resp_register.status_code == 201
        # registered user login
        resp_login = client.post(
            '/auth/login',
            json={
                'email': 'joesssd@gmail.com',
                'password': '123456',
            }
        )
        data = json.loads(resp_login.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content']['auth_token']
        assert resp_login.content_type == 'application/json'
        assert resp_login.status_code == 200
        # time.sleep(6)
        response = client.post(
            '/auth/logout',
            headers={
                'Authorization': f'Bearer {data["content"]["auth_token"]}s'
            },
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['code'] == 901
        assert data['msg'] == 'Invalid request'
        # assert response.content_type == 'application/json'
        assert response.status_code == 401