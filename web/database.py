import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = (create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(
    os.environ['DATABASE_USER'],
    os.environ['DATABASE_PASSWORD'],
    os.environ['DATABASE_HOST'],
    os.environ['DATABASE_PORT'],
    os.environ['DATABASE_NAME']
)))

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models
    import models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open('fixtures/substances.json') as f:
        data = f.read()
        data = json.loads(data)
        for item in data:
            s = models.Substance(**item)
            db_session.add(s)
        db_session.commit()
    with open('fixtures/latent_heats.json') as f:
        data = f.read()
        data = json.loads(data)
        for item in data:
            p = models.LatentHeats(**item)
            db_session.add(p)
        db_session.commit()


if __name__ == '__main__':
    init_db()
