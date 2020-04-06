from marshmallow import Schema, fields, post_load

from app import db
from app.helpers import hash_password, EnumField


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


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class DrawSourceSchema(Schema):
    id = fields.UUID()
    type = EnumField(enum=db.DrawSourceType)
    name = fields.Str()
    company_id = fields.UUID()
    color = fields.Str()
    code = fields.Str()
    color_category = fields.Str()


class DrawSourceCreateSchema(Schema):
    type = EnumField(enum=db.DrawSourceType, required=True)
    name = fields.Str(required=True)
    company_id = fields.Str(required=True)
    color = fields.Str(required=True)
    code = fields.Str(required=True)
    color_category = fields.Str()
