from aiopg import Cursor
from aiopg.sa import Engine
from aiopg.sa.result import RowProxy
from marshmallow import Schema, fields, post_load

import db
from helpers import hash_password, EnumField


class UserSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


class RegisterSchema(Schema):
    name = fields.Str(default='')
    phone = fields.Str(default='')
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


class DrawSourceSchema(Schema):
    id = fields.UUID()
    type = EnumField(enum=db.DrawSourceType)
    company = fields.Str()
    color = fields.Str()
    code = fields.Str()


class DrawSourceCreateSchema(Schema):
    type = EnumField(enum=db.DrawSourceType, required=True)
    company = fields.Str(required=True)
    color = fields.Str(required=True)
    code = fields.Str(required=True)
