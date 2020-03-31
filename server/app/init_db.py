import db

if __name__ == '__main__':
    engine = db.get_sync_engine()
    db.meta.create_all(bind=engine)
