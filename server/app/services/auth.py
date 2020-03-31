import datetime

import jwt

from settings import config


class AuthService:
    @staticmethod
    def create_access_token(user: dict) -> str:
        payload = {
            **user,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config['jwt']['access_exp']),
        }
        return jwt.encode(payload, config['jwt']['secret'], 'HS256').decode('utf-8')

    @staticmethod
    def create_refresh_token(user: dict) -> str:
        payload = {
            **user,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config['jwt']['refresh_exp']),
        }
        return jwt.encode(payload, config['jwt']['secret'], 'HS256').decode('utf-8')

    @staticmethod
    def get_token_payload(token: str) -> dict:
        return jwt.decode(token, config['jwt']['secret'], algorithms='HS256')

    @classmethod
    def refresh_token(cls, token: str) -> str:
        payload = cls.get_token_payload(token)
        return cls.create_access_token(payload)
