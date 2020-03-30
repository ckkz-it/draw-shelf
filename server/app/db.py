import datetime
from uuid import uuid4

from aiohttp.web_app import Application
from aiopg.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

__all__ = ['user']

meta = MetaData()

user = Table(
    'user', meta,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('name', Text, nullable=False),
    Column('email', Text, nullable=False, unique=True),
    Column('phone', Text, nullable=False),
    Column('password', Text, nullable=False),
    Column('created_at', DateTime, nullable=False, default=datetime.datetime.utcnow),
)


async def init_pg(app: Application) -> None:
    conf = app['config']['postgres']
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app: Application) -> None:
    app['db'].close()
    await app['db'].wait_closed()
