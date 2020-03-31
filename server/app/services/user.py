from aiopg import Cursor
from aiopg.sa import Engine
from aiopg.sa.result import RowProxy

import db
from helpers import verify_password
from serializers import UserSchema


class UserService:
    @staticmethod
    async def get_authenticated_user(engine: Engine, email: str, password: str) -> tuple:
        try:
            async with engine.acquire() as conn:
                cursor: Cursor = await conn.execute(db.user.select(db.user.c.email == email))
                result: RowProxy = await cursor.fetchone()
                if result:
                    if verify_password(password, result.get('password')):
                        return UserSchema().dump(result), False
                return None, True
        except Exception as e:
            return e, True
