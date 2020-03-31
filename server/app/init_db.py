import db
from utils.password import hash_password


def create_tables(eng):
    db.meta.create_all(bind=eng)


def sample_data(eng):
    user = {
        'name': 'Andrey Laguta',
        'email': 'cirkus.kz@gmail.com',
        'phone': '+375 29 999 99 99',
        'password': hash_password('qwerty'),
    }
    conn = eng.connect()
    conn.execute(db.user.insert().values(**user))


if __name__ == '__main__':
    engine = db.get_sync_engine()
    create_tables(engine)
    sample_data(engine)
