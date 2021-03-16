import json
import pytest
import unittest

# from pytest import TestCase
from tests.client import seclient
# from myapp.model.users import User
from myapp.model.articles import Article
from myapp.model.article_tag import ArticleTag
from myapp.model.tags import Tag
from myapp.database import db_session


class TestUserArticle:
    # default add Authorization token

    def test_create_fail_article(self, seclient):
        """
        GIVEN url path
        WHEN 
        THEN get articles list
        """
        create_res = seclient.post(
            '/api/article/edit',
            headers={
                'Content-Type': 'application/json',
            },
            json={
                'title': 'Test title',
            }
        )
        data = json.loads(create_res.data)
        assert data['code'] == 904
        # assert data['msg'] == 'ok'
        assert create_res.status_code == 404
        assert create_res.content_type == 'application/json'

    def test_create_get_list_edit_get_article(self, seclient):
        """
        Test create, get list, edit, get detail
        """
        create_res = seclient.post(
            '/api/article/edit',
            headers={
                'Content-Type': 'application/json',
            },
            json={
                'title': 'Test title',
                'contents': 'あいうえお, 12345 你我他 test end.',
                'tags': "123,456,test,t1"
            }
        )
        create_res_data = json.loads(create_res.data)
        assert create_res_data['code'] == 0
        assert create_res_data['msg'] == 'ok'
        assert create_res.status_code == 201
        assert create_res.content_type == 'application/json'
        # get exists articles
        response = seclient.get(
            '/api/article',
            headers={
                'Content-Type': 'application/json'
            }
        )
        articles_data = json.loads(response.data)
        assert articles_data['code'] == 0
        assert articles_data['msg'] == 'ok'
        assert articles_data['content'] is not None
        assert type(articles_data['content']) is list
        assert type(articles_data['content'][0]['id']) is int
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        # edit exists article
        article_id = articles_data['content'][0]['id']
        response = seclient.post(
            f'/api/article/edit?id={article_id}', 
            headers={
                'Content-Type': 'application/json'
            },
            json={
                'title': 'Test title edited.',
                'contents': 'あいうえお, 12345 你我他 test end. Edited.',
                'tags': "123,456,test,t14564"
            }
        )
        edit_data = json.loads(response.data)
        assert edit_data['code'] == 0
        assert edit_data['msg'] == 'ok'
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        # get exists article
        response = seclient.get(
            f'/api/article?id={article_id}',
            headers={
                'Content-Type': 'application/json'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert data['content'] is not None
        assert data['content']['title'] == 'Test title edited.'
        assert data['content']['contents'] == 'あいうえお, 12345 你我他 test end. Edited.'
        assert data['content']['tags'] == "123,456,test,t14564"
        assert response.status_code == 200
        assert response.content_type == 'application/json'

    def test_error_article(self, seclient, request):
        """
        GIVEN authorization
        WHEN invalid parm or data
        THEN get correct response
        """
        response = seclient.get(
            '/api/article',
            headers={
                'Content-Type': 'application/json'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['msg'] == 'ok'
        assert type(data.get('content')) is list
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        # get not exist article
        response = seclient.get(
            '/api/article?id=xxxx',
            headers={
                'Content-Type': 'application/json'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 902
        # assert data['msg'] == 'ok'
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        # edit error parm
        response = seclient.get(
            '/api/article?id=xxxx',
            headers={
                'Content-Type': 'application/json'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 902
        # assert data['msg'] == 'ok'
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        # delete parm
        response = seclient.delete(
            '/api/article',
            headers={
                'Content-Type': 'application/json'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 902
        # assert data['msg'] == 'ok'
        assert response.status_code == 403
        assert response.content_type == 'application/json'
        # delete parm
        response = seclient.delete(
            '/api/article?id=xxxxxx',
            headers={
                'Content-Type': 'application/json'
            },
        )
        data = json.loads(response.data)
        assert data['code'] == 902
        # assert data['msg'] == 'ok'
        assert response.status_code == 404
        assert response.content_type == 'application/json'