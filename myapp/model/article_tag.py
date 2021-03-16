from conf import settings
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY
from typing import Union, Any
from myapp.database import Base
import datetime
import logging


class ArticleTag(Base):
    __tablename__ = 'article_tag'
    article_id = Column(Integer, nullable=False, primary_key=True)
    tag = Column(String(50), nullable=False, primary_key=True)

    log = logging.getLogger('ArticleTagModel')

    def __init__(self, article_id=None, tag=None):
        self.article_id = article_id
        self.tag = tag

    def __repr__(self):
        return f'<ArticleId {self.article_id}, Tag {self.tag}>'

    def to_dict(self):
        info = self.__dict__
        if '_sa_instance_state' in info:
            del info['_sa_instance_state']
        return info