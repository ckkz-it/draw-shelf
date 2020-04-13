import json
import pathlib
from argparse import ArgumentParser

import sqlalchemy as sa

from app import db
from app.helpers import hash_password

BASE_DIR = pathlib.Path(__file__).parent.parent
fixtures_dir = BASE_DIR / 'fixtures'
markers_file = fixtures_dir / 'markers.json'


def recreate_dbs(eng: sa.engine.Engine):
    db.meta.drop_all(bind=eng)
    db.meta.create_all(bind=eng)


def create_ds_from_fixtures(eng: sa.engine.Engine, file) -> sa.engine.ResultProxy:
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
                res: sa.engine.ResultProxy = eng.execute(
                    db.company.insert().values(name=company_name).returning(db.company.c.id)
                )
                company_id = str(res.first().id)
            draw_source_to_insert.extend(map(lambda x: {**x, 'company_id': company_id}, company_ds))

    created_ds: sa.engine.ResultProxy = eng.execute(
        db.draw_source.insert().values(draw_source_to_insert).returning(db.draw_source.c.id)
    )
    return created_ds


def assign_ds_to_user(eng: sa.engine.Engine, drw_srcs: sa.engine.ResultProxy, u_id):
    relations_to_insert = [{'user_id': u_id, 'draw_source_id': ds.id} for ds in drw_srcs]
    eng.execute(db.user_draw_source_relationship.insert().values(relations_to_insert))


def create_user(eng: sa.engine.Engine):
    user = {
        'name': 'User',
        'email': 'user@test.com',
        'password': hash_password('qwerty'),
        'phone': '123321123',
    }
    res: sa.engine.ResultProxy = eng.execute(db.user.insert().values(user).returning(db.user.c.id))
    return res.first().id


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--recreate_dbs', '-rc', action='store_true')
    arg_parser.add_argument('--create_user', '-u', action='store_true')
    arg_parser.add_argument('--create_draw_sources', '-ds', action='store_true')
    arg_parser.add_argument('--assign_user_to_ds', '-autds', default=None)
    args = arg_parser.parse_args()

    engine = db.get_sync_engine()
    res_user = engine.execute(db.user.select()).first()
    user_id = res_user.id if res_user else None
    draw_sources = engine.execute(db.draw_source.select())

    if args.recreate_dbs:
        recreate_dbs(engine)
    if args.create_user:
        user_id = create_user(engine)
    if args.create_draw_sources:
        draw_sources = create_ds_from_fixtures(engine, markers_file)
    if args.assign_user_to_ds:
        if args.assign_user_to_ds.lower() not in ['true', 't', 'y', 'yes']:  # user's id was passed
            user_id = args.assign_user_to_ds
        assign_ds_to_user(engine, draw_sources, user_id)
