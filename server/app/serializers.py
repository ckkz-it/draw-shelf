import typing

from aiohttp_rest_framework import exceptions, fields
from aiohttp_rest_framework.serializers import ModelSerializer

from marshmallow import post_load

from app import db
from app.helpers.password import hash_password, verify_password


class UserSerializer(ModelSerializer):
    id = fields.UUID(read_only=True)
    password = fields.Str(write_only=True)
    created_at = fields.DateTime(read_only=True)

    class Meta:
        model = db.user
        fields = ('id', 'name', 'phone', 'email', 'password', 'created_at')

    @post_load
    def hash_password(self, data, **_):
        if 'password' in data:
            return {**data, 'password': hash_password(data['password'])}
        return data


class LoginSerializer(ModelSerializer):
    class Meta:
        model = db.user
        fields = ('email', 'password')

    async def save(self, **kwargs):
        db_service = await self.get_db_service()
        try:
            user = await db_service.get(email=self.validated_data['email'])
        except exceptions.ObjectNotFound:
            return None
        if verify_password(self.validated_data['password'], user.password):
            return UserSerializer(user).data
        return None


class CompanySerializer(ModelSerializer):
    id = fields.UUID()
    name = fields.Str()

    class Meta:
        model = db.company
        fields = '__all__'


class DrawSourceSerializer(ModelSerializer):
    companies = fields.Nested(CompanySerializer, data_key='company')

    class Meta:
        model = db.draw_source
        fields = ('id', 'type', 'name', 'companies', 'color', 'code', 'color_category')


class DrawSourceForUserSerializer(DrawSourceSerializer):
    quantity = fields.Int()
    resource = fields.Enum(db.DrawSourceResource)

    class Meta(DrawSourceSerializer.Meta):
        fields = (
            'id', 'type', 'name', 'companies', 'color', 'code', 'color_category', 'quantity', 'resource'
        )

    async def update(self, instance, validated_data: typing.OrderedDict):
        from app.services.draw_source import DrawSourceService

        engine = self.serializer_context['view'].engine
        user = self.serializer_context['view'].user
        service = DrawSourceService(engine)
        await service.update(instance['id'], validated_data)
        return await service.get_for_user(user['id'], instance['id'])


class DrawSourceCreateSerializer(ModelSerializer):
    quantity = fields.Int()
    resource = fields.Enum(db.DrawSourceResource)

    class Meta:
        model = db.draw_source
        fields = ('type', 'name', 'company_id', 'color', 'code', 'color_category', 'quantity', 'resource')


class UserDrawSourceRelationshipSerializer(ModelSerializer):
    class Meta:
        model = db.udsr
        fields = '__all__'
