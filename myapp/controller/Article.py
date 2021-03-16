import json
import logging
import traceback
from flask import request, g
from flask.globals import session
from flask.views import MethodView
from myapp.common.Response import response
from myapp.common.ReturnCode import ReturnError
from myapp.model.users import User
from myapp.model.articles import Article
from myapp.model.article_tag import ArticleTag
from myapp.model.tags import Tag
from myapp.database import db_session
from sqlalchemy.sql import select, null
from schema import Schema, And, Optional, SchemaError


class ArticleVerification:
    @staticmethod
    def post_add_and_edit_article(data):
        try:
            schema = Schema({
                'title': And(str, lambda s: len(s) < 100),
                'contents': And(str, lambda s: len(s) < 65535),
                'tags': And(str, lambda s: len(s.split(" ")) < 10),
                })
            validated = schema.validate(data)
            validated['tags'] = validated['tags'].split(" ")
            return validated
        except SchemaError as _:
            raise ReturnError(903)


class ArticleAPI(MethodView):
    log = logging.getLogger('ArticleAPI')
    def get(self):
        self.log.info('ArticleAPI get')
        article_id = request.args.get('id')
        if article_id:
            article = Article.query.filter(User.id==g.user_id, Article.id==article_id).first()
            self.log.info(article)
            if article is None:
                return response(404, 902)
            content = article.to_dict()
            article_tags = ArticleTag.query.filter(ArticleTag.article_id==article_id).all()
            if article_tags:
                tags = ''
                for r in article_tags:
                    tags = f'{tags},{r.tag}' if tags else f'{r.tag}'
                content.update({'tags': tags}) if tags else content.update({'tags': ''})

            self.log.debug(content)
            return response(200, 0, content=content)
        else:
            # s = select([Article.id, Article.title, Article.created_on]).where(Article.user_id==g.user_id)
            # results = db_session.execute(s)
            articles = db_session.query(Article.id, Article.title, Article.created_on).filter(Article.user_id==g.user_id).all()
            self.log.debug(Article)
            content = []
            for r in articles:
                self.log.debug(r)
                content.append({
                    'id': r[0],
                    'title': r[1],
                    'created_on': r[2]
                })

            return response(200, 0, content=content)

    def post(self):
        self.log.info('ArticleAPI post')
        article_id = request.args.get('id')
        data = request.get_json()
        data = ArticleVerification.post_add_and_edit_article(data)
        try:
            if article_id:
                # article = Article.query.filter(Article.id==article_id).first()
                article = db_session.query(Article).filter(Article.id==article_id).first()
                article.title = data['title']
                article.contents = data['contents']
                # tag check and add
                tag_objs = []
                for tag in data['tags']:
                    tag_obj = db_session.query(Tag).filter(Tag.tag==tag).first()
                    if tag_obj is None:
                        tag_obj = Tag(tag)
                        db_session.add(tag_obj)
                    tag_objs.append(tag_obj)
                # articleTag delete first, and add
                db_session.query(ArticleTag).filter(ArticleTag.article_id==article_id).\
                    delete(synchronize_session=False)
                article_tags = []
                for tag_obj in tag_objs:
                    article_tag = ArticleTag(article.id, tag_obj.tag)
                    article_tags.append(article_tag)
                db_session.add_all(article_tags)

                db_session.commit()
                return response(200, 0)
            else:
                article = Article(g.user_id, data['title'], data['contents'])
                db_session.add(article)
                db_session.commit()
                # tag check and add
                tag_objs = []
                for tag in data['tags']:
                    exist_tag = db_session.query(Tag).filter(Tag.tag==tag).first()
                    if not exist_tag:
                        tag_obj = Tag(tag)
                        tag_objs.append(tag_obj)
                db_session.add_all(tag_objs)
                # artickeTag check
                article_tags = []
                for tag_obj in tag_objs:
                    article_tag = ArticleTag(article.id, tag_obj.tag)
                    article_tags.append(article_tag)
                db_session.add_all(article_tags)
                db_session.commit()
                return response(201, 0)
        except Exception as e:
            # self.log.debug(e)
            self.log.debug(traceback.format_exc().replace("\n", ""))
            return response(404, 1)

    def delete(self):
        self.log.info('ArticleAPI delete')
        article_id = request.args.get('id')
        try:
            if article_id:
                article = db_session.query(Article).filter(Article.id==article_id, Article.user_id==g.user_id).first()
                if article:
                    db_session.delete(article)
                    db_session.commit()
                    return response(201, 0)
                else:
                    return response(404, 902)
            else:
                return response(403, 902)
                # raise ReturnError(902)
        except ReturnError as e:
            return response(403, e.code, e.msg)
        except Exception as e:
            # self.log.debug(e)
            self.log.debug(traceback.format_exc().replace("\n", ""))
            return response(404, 1)
