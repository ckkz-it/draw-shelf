from sqlalchemy import create_engine, MetaData

from app.settings import config
from app.db import user
from app.utils import hash_password

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[user])


def sample_data(eng):
    conn = eng.connect()
    conn.execute(user.insert(), [
        {
            'name': 'Andrey Laguta',
            'email': 'cirkus.kz@gmail.com',
            'phone': '+375 29 999 99 99',
            'password': hash_password('qwerty'),
        },
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
