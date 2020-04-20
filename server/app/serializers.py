from marshmallow import EXCLUDE, Schema, fields, post_load

from app import db
from app.helpers.fields import EnumField
from app.helpers.password import hash_password


class UserSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    class Meta:
        ordered = True


class RegisterSchema(Schema):
    name = fields.Str(default='')
    phone = fields.Str(default='')
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def hash_password(self, data, **_):
        return {**data, 'password': hash_password(data['password'])}


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class CompanySchema(Schema):
    id = fields.UUID()
    name = fields.Str()

    class Meta:
        ordered = True


class DrawSourceSchema(Schema):
    id = fields.UUID()
    type = EnumField(enum=db.DrawSourceType)
    name = fields.Str()
    companies = fields.Nested(CompanySchema, data_key='company')
    color = fields.Str()
    code = fields.Str()
    color_category = fields.Str()

    class Meta:
        ordered = True
        unknown = EXCLUDE


class DrawSourceForUserSchema(DrawSourceSchema):
    quantity = fields.Int()
    resource = EnumField(enum=db.DrawSourceResource)


class DrawSourceCreateSchema(Schema):
    type = EnumField(enum=db.DrawSourceType, required=True)
    name = fields.Str(required=True)
    company_id = fields.Str(required=True)
    color = fields.Str(required=True)
    code = fields.Str(required=True)
    color_category = fields.Str()
    quantity = fields.Int()
    resource = EnumField(enum=db.DrawSourceResource)


class UserDrawSourceRelationshipSchema(Schema):
    draw_source_id = fields.UUID()
    user_id = fields.UUID()
    quantity = fields.Int()
    resource = EnumField(enum=db.DrawSourceResource)

    class Meta:
        unknown = EXCLUDE
