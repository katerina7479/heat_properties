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


def create_fixtures():
    '''Create fixtures from comma-separated data'''
    with open('fixtures/data.txt') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            item = {}
            try:
                line = [x.strip() for x in line.split(',')]
                item['symbol'], item['name'], item['mp'], item['hf'], item['bp'], item['hv'] = [x if x != 'none' else None for x in line]
                data.append(item)
            except:
                print "Error", line

    substance_data = []
    heat_data = []
    for i, item in enumerate(data):
        substance_data.append({'id': i, 'name': item['name'].lower(), 'symbol': item['symbol']})

        for k in ['mp', 'bp', 'hf', 'hv']:
            if item[k]:
                if k in ['mp', 'bp']:
                    item[k] = float(item[k])
                else:
                    item[k] = int(item[k])

        heat_data.append({"substance_id": i,
                          "melting_point": item['mp'],
                          "boiling_point": item['bp'],
                          "heat_of_fusion": item['hf'],
                          "heat_of_vaporization": item['hv']})

    with open('fixtures/substances.json', 'w') as f:
        f.write(json.dumps(substance_data))

    with open('fixtures/latent_heats.json', 'w') as f:
        f.write(json.dumps(heat_data))


def load_fixtures():
    import models
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


def init_db():
    # import all modules here that might define models
    import models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
    load_fixtures()
