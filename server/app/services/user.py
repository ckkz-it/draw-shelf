from sqlalchemy import select

from app import db
from app.helpers import verify_password, DBDataParser
from app.serializers import UserSchema, DrawSourceSchema
from app.services.mixins import ModelServiceMixin


class UserService(ModelServiceMixin):
    db_table = db.user
    schema = UserSchema

    async def create(self, user_data: dict) -> tuple:
        try:
            user = await self._create(user_data, return_created_obj=True)
        except Exception as e:
            return None, e
        return self.schema().dump(user), None

    async def get_authenticated_user(self, email: str, password: str) -> tuple:
        try:
            result = await self._get_one(db.user.c.email == email)
            if result:
                if verify_password(password, result.get('password')):
                    return UserSchema().dump(result), False
            return None, True
        except Exception as e:
            return e, True

    async def get_draw_sources(self, user_id: str):
        try:
            query = select([db.draw_source, db.company], use_labels=True) \
                .select_from(db.draw_source.join(db.company))
            result = await self._get_all_custom(query)
            name_mapping = dict(companies='company')
            data = DBDataParser(result, 'draw_sources', many=True, name_mapping=name_mapping).parse()
            return DrawSourceSchema(many=True).dump(data)
        except Exception as e:
            raise e
