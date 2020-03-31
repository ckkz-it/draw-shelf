import datetime
from typing import Optional

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
    def get_token_payload(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, config['jwt']['secret'], algorithms='HS256')
        except jwt.ExpiredSignature:
            return None
