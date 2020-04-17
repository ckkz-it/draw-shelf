import typing
from aiopg.sa import Engine

from app import db
from app.helpers.password import verify_password
from app.serializers import UserSchema
from app.services.database import DatabaseService


class UserService:
    schema = UserSchema
    db_service: DatabaseService = None

    def __init__(self, engine: Engine):
        self.db_service = DatabaseService(engine, db.user)

    async def create(self, user_data: dict) -> dict:
        user = await self.db_service.create(user_data, return_created_obj=True)
        return self.schema().dump(user)

    async def get_authenticated_user(self, email: str, password: str) -> typing.Optional[dict]:
        result = await self.db_service.get_one(db.user.c.email == email)
        if result:
            if verify_password(password, result.get('password')):
                return self.schema().dump(result)
        return None
