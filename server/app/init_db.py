import json
import pathlib

import sqlalchemy as sa

from app import db
from app.helpers import hash_password

BASE_DIR = pathlib.Path(__file__).parent.parent
fixtures_dir = BASE_DIR / 'fixtures'
markers_file = fixtures_dir / 'markers.json'


def recreate_dbs(eng: sa.engine.Engine):
    db.meta.drop_all(bind=eng)
    db.meta.create_all(bind=eng)


def create_ds_from_fixtures(file, eng: sa.engine.Engine):
    with open(file) as f:
        data = json.loads(f.read())

    draw_source_to_insert = []
    for company_item in data:
        for company_name, company_ds in company_item.items():
            res: sa.engine.ResultProxy = eng.execute(db.company.select(db.company.c.name == company_name))
            company_id = None
            if res.rowcount == 1:
                company_id = str(res.first().id)
            else:
                company: sa.engine.ResultProxy = eng.execute(
                    db.company.insert().values(name=company_name).returning(db.company.c.id)
                )
                company_id = str(company.first().id)
            draw_source_to_insert.extend(map(lambda x: {**x, 'company_id': company_id}, company_ds))

    eng.execute(db.draw_source.insert().values(draw_source_to_insert))


def create_user(eng: sa.engine.Engine):
    user = {
        'name': 'User',
        'email': 'user@test.com',
        'password': hash_password('qwerty'),
        'phone': '123321123',
    }
    eng.execute(db.user.insert().values(user))


if __name__ == '__main__':
    engine = db.get_sync_engine()
    # recreate_dbs(engine)
    create_ds_from_fixtures(markers_file, engine)
