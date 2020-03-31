from aiopg import Cursor
from aiopg.sa import Engine
from aiopg.sa.result import RowProxy
from marshmallow import Schema, fields, post_load

import db
from exceptions import AuthenticationFailed
from utils.password import hash_password, verify_password


class UserSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


class RegisterSchema(Schema):
    name = fields.Str(required=False, default='')
    phone = fields.Str(required=False, default='')
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def hash_password(self, data, **kwargs):
        return {**data, 'password': hash_password(data['password'])}

    @staticmethod
    async def create_user(engine: Engine, user_data: dict) -> tuple:
        try:
            async with engine.acquire() as conn:
                await conn.execute(db.user.insert().values(**user_data))
                cursor: Cursor = await conn.execute(db.user.select().order_by(db.user.c.id))
                result: RowProxy = await cursor.fetchone()
                return UserSchema().dump(result), None
        except Exception as e:
            return None, e


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    @staticmethod
    async def get_authenticated_user(engine: Engine, user_data: dict):
        try:
            async with engine.acquire() as conn:
                cursor: Cursor = await conn.execute(db.user.select(db.user.c.email == user_data['email']))
                result: RowProxy = await cursor.fetchone()
                if result:
                    if verify_password(user_data['password'], result.get('password')):
                        return UserSchema().dump(result), None
                raise AuthenticationFailed
        except Exception as e:
            return None, e


class DrawSourceSchema(Schema):
    id = fields.UUID()
    type = fields.Str()
    company = fields.Str()
    color = fields.Str()
