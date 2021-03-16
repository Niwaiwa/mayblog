from conf import settings
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY
from typing import Union, Any
from myapp.database import Base
import datetime
import logging


class Tag(Base):
    __tablename__ = 'tags'
    tag = Column(String(50), primary_key=True, unique=True, nullable=False)

    log = logging.getLogger('TagModel')

    def __init__(self, tag=None):
        self.tag = tag

    def __repr__(self):
        return '<Article %r>' % (self.tag)

    def to_dict(self):
        info = self.__dict__
        if '_sa_instance_state' in info:
            del info['_sa_instance_state']
        return info