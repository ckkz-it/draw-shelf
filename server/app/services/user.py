from aiopg.sa import Engine
from sqlalchemy import select

from app import db
from app.helpers import verify_password, DBDataParser
from app.serializers import UserSchema, DrawSourceForUserSchema
from app.services.database import DatabaseService


class UserService:
    schema = UserSchema
    db_service: DatabaseService = None

    def __init__(self, engine: Engine):
        self.db_service = DatabaseService(engine, db.user)

    async def create(self, user_data: dict) -> tuple:
        try:
            user = await self.db_service.create(user_data, return_created_obj=True)
        except Exception as e:
            return None, e
        return self.schema().dump(user), None

    async def get_authenticated_user(self, email: str, password: str) -> tuple:
        try:
            result = await self.db_service.get_one(db.user.c.email == email)
            if result:
                if verify_password(password, result.get('password')):
                    return self.schema().dump(result), False
            return None, True
        except Exception as e:
            return e, True

    async def get_draw_sources(self, user_id: str):
        try:
            query = select([db.user_draw_source_relationship.c.resource,
                            db.user_draw_source_relationship.c.quantity,
                            db.draw_source, db.company], use_labels=True) \
                .select_from(db.user_draw_source_relationship.join(db.draw_source.join(db.company))) \
                .where(db.user_draw_source_relationship.c.user_id == user_id)
            result = await self.db_service.get_all_custom(query)
            data = DBDataParser(result, ['draw_sources', 'users_draw_sources'], many=True).parse()
            return DrawSourceForUserSchema(many=True).dump(data)
        except Exception as e:
            raise e
