from app import db
from app.helpers import verify_password
from app.serializers import UserSchema
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
