import enum
from typing import Optional

import aiopg.sa
import sqlalchemy as sa
from aiohttp.web_app import Application
from sqlalchemy.dialects.postgresql import UUID

from settings import config
from utils.helpers import stringified_uuid

engine: Optional[aiopg.sa.Engine] = None
sync_engine: Optional[sa.engine.Engine] = None

DB_URL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**config['postgres'])


async def get_engine() -> aiopg.sa.Engine:
    global engine
    if not engine:
        engine = await aiopg.sa.create_engine(DB_URL)
    return engine


def get_sync_engine() -> sa.engine.Engine:
    global sync_engine
    if not sync_engine:
        sync_engine = sa.create_engine(DB_URL)
    return sync_engine


async def init_pg(app: Application) -> None:
    app['db'] = await get_engine()


async def close_pg(app: Application) -> None:
    app['db'].close()
    await app['db'].wait_closed()


meta = sa.MetaData()

user_draw_source_relationship = sa.Table(
    'users_draw_sources', meta,
    sa.Column('user_id', UUID, sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('source_id', UUID, sa.ForeignKey('draw_sources.id'), primary_key=True),
)

user = sa.Table(
    'users', meta,
    sa.Column('id', UUID, primary_key=True, default=stringified_uuid),
    sa.Column('name', sa.Text, nullable=False),
    sa.Column('email', sa.Text, nullable=False, unique=True),
    sa.Column('phone', sa.Text, nullable=False),
    sa.Column('password', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()')),
)


class DrawSourceType(enum.Enum):
    marker = 'marker',
    paints = 'paints',


draw_source = sa.Table(
    'draw_sources', meta,
    sa.Column('id', UUID, primary_key=True, default=stringified_uuid),
    sa.Column('type', sa.Enum(DrawSourceType), nullable=False),
    sa.Column('color', sa.Text, nullable=False),
    sa.Column('company', sa.Text, nullable=False),
)
