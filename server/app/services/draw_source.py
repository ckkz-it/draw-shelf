from aiopg.sa import Engine

from sqlalchemy import and_, select

from app import db
from app.app_types import FETCH
from app.helpers.utils import DBDataParser
from app.serializers import DrawSourceSerializer, UserDrawSourceRelationshipSerializer
from app.services.database import DatabaseService


class DrawSourceService:
    serializer = DrawSourceSerializer
    db_service: DatabaseService = None

    def __init__(self, engine: Engine):
        self.db_service = DatabaseService(engine, db.draw_source)

    async def update(self, ds_id: str, data: dict):
        # update draw_source related data
        ds_data = self.serializer(exclude=['companies']).to_representation(data)
        await self.db_service.update(ds_data, where=db.draw_source.c.id == ds_id)
        # update users_draw_sources relationship related data
        udsr_data = UserDrawSourceRelationshipSerializer().to_representation(data)
        query = db.udsr.update(db.udsr.c.draw_source_id == ds_id).values(udsr_data)
        await self.db_service.execute(query)

    async def get_for_user(self, user_id: str, ds_id: str = None, *, many=False):
        query = select([db.udsr.c.resource, db.udsr.c.quantity, db.draw_source, db.company], use_labels=True) \
            .select_from(db.udsr.join(db.draw_source.join(db.company))) \
            .order_by(db.draw_source.c.code)
        if many:
            query = query.where(db.udsr.c.user_id == user_id)
            fetch = FETCH.all
        else:
            query = query.where(and_(db.udsr.c.user_id == user_id, db.udsr.c.draw_source_id == ds_id))
            fetch = FETCH.one
        result = await self.db_service.execute(query, fetch=fetch)
        data = DBDataParser(result, ['draw_sources', 'users_draw_sources'], many=many).parse()
        return data
