import datetime
import enum
from typing import Optional
from uuid import uuid4

import aiopg.sa
import sqlalchemy as sa
from aiohttp.web_app import Application
from sqlalchemy.dialects.postgresql import UUID

from app.settings import config

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


class DrawSourceResource(enum.Enum):
    empty = 'empty'
    low = 'low'
    half = 'half'
    full = 'full'


user_draw_source_relationship = sa.Table(
    'users_draw_sources', meta,
    sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('draw_source_id', UUID(as_uuid=True), sa.ForeignKey('draw_sources.id'), primary_key=True),
    sa.Column('resource', sa.Enum(DrawSourceResource, name='draw_source_resource'), nullable=True,
              default=DrawSourceResource.full),
    sa.Column('quantity', sa.Integer, nullable=False, default=1),
)

user = sa.Table(
    'users', meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    sa.Column('name', sa.Text, nullable=False, default=''),
    sa.Column('email', sa.Text, nullable=False, unique=True, default=''),
    sa.Column('phone', sa.Text, nullable=False, default=''),
    sa.Column('password', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.datetime.utcnow),
)

company = sa.Table(
    'companies', meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    sa.Column('name', sa.Text, nullable=False),
)


class DrawSourceType(enum.Enum):
    marker = 'marker',
    paints = 'paints',


draw_source = sa.Table(
    'draw_sources', meta,
    sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    sa.Column('type', sa.Enum(DrawSourceType, name='draw_source_type'), nullable=False),
    sa.Column('name', sa.Text, nullable=False),
    sa.Column('color', sa.Text, nullable=False),
    sa.Column('code', sa.Text, nullable=False),
    sa.Column('color_category', sa.Text, nullable=False, default=''),
    sa.Column('company_id', sa.ForeignKey('companies.id'), nullable=True),
)
