import datetime

import jwt

from app.settings import config


class AuthService:
    jwt_cfg = config['jwt']

    @classmethod
    def create_access_token(cls, user: dict) -> str:
        payload = {
            'user': user,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=cls.jwt_cfg['access_exp']),
        }
        return jwt.encode(payload, cls.jwt_cfg['secret'], cls.jwt_cfg['algorithm']).decode('utf-8')

    @classmethod
    def create_refresh_token(cls, user: dict) -> str:
        payload = {
            'user': user,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=cls.jwt_cfg['refresh_exp']),
        }
        return jwt.encode(payload, cls.jwt_cfg['secret'], cls.jwt_cfg['algorithm']).decode('utf-8')

    @classmethod
    def get_token_payload(cls, token: str) -> dict:
        return jwt.decode(token, cls.jwt_cfg['secret'], algorithms=[cls.jwt_cfg['algorithm']])

    @classmethod
    def refresh_token(cls, token: str) -> str:
        payload = cls.get_token_payload(token)
        return cls.create_access_token(payload['user'])
