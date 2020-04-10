import json
import pathlib

from sqlalchemy.engine import Engine

from app import db

BASE_DIR = pathlib.Path(__file__).parent.parent
fixtures_dir = BASE_DIR / 'fixtures'
markers_file = fixtures_dir / 'markers.json'


def create_dbs(eng: Engine):
    db.meta.drop_all(bind=eng)
    db.meta.create_all(bind=eng)


def create_ds_from_fixtures(file, eng: Engine):
    with open(file) as f:
        data = json.loads(f.read())
    eng.execute(db.draw_source.insert().values(data))


if __name__ == '__main__':
    engine = db.get_sync_engine()
    create_dbs(engine)
    create_ds_from_fixtures(markers_file, engine)
