from app import db

engine = db.get_sync_engine()
db.meta.create_all(bind=engine)
