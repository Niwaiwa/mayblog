from conf import settings
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from typing import Union, Any
from myapp.database import Base
from myapp.utils.Secrets import Secrets
from myapp.common.ReturnCode import ReturnError
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from hashlib import sha256
import datetime
import jwt
import logging


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    log = logging.getLogger('UserModel')

    def __init__(self, name=None, email=None, password=None, admin=False):
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password=password).decode() if password else \
            Bcrypt().generate_password_hash(password=Secrets.generate_password()).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '<User %r>' % (self.name)

    def to_dict(self):
        info = self.__dict__
        if '_sa_instance_state' in info:
            del info['_sa_instance_state']
        return info

    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def encode_auth_token(self, user_id: str, expire_sec: int = settings.login_expire_sec) -> Any:
        """
        Generates the Auth Token
        :return: string
        """
        self.log.info('encode_auth_token')
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_sec),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'iss': 'test.com',
            }
            return jwt.encode(
                payload,
                settings.secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            raise ReturnError(1, str(e))

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        User.log.info('decode_auth_token')
        try:
            payload = jwt.decode(
                auth_token,
                settings.secret_key,
                algorithms='HS256',
                issuer='test.com'
            )
            # User.log.info(payload)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise ReturnError(11, 'Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise ReturnError(11, 'Invalid token. Please log in again.')
