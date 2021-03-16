from conf import settings
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, TEXT
from typing import Text, Union, Any
from myapp.database import Base
import datetime
import logging


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    contents = Column(TEXT, nullable=True)
    created_on = Column(DateTime, nullable=False)

    log = logging.getLogger('ArticleModel')

    def __init__(self, user_id=None, title=None, contents=None):
        self.user_id = user_id
        self.title = title
        self.contents = contents
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return '<Article %r>' % (self.title)

    def to_dict(self):
        info = self.__dict__
        if '_sa_instance_state' in info:
            del info['_sa_instance_state']
        return info