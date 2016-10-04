'''Database functions for use with Flask app'''
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Define Database engine and connection to mysql
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


def _heat_fixtures():
    '''Create the heat fixtures'''
    # Get the data from heat_data
    with open('fixtures/heat_data.txt') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            item = {}
            line = [x.strip() for x in line.split(',')]
            item['symbol'], item['name'], item['mp'], item['hf'], item['bp'], item['hv'] = [x if x != 'none' else None for x in line]
            data.append(item)

    # Map to json
    substance_data = []
    heat_data = []
    for i, item in enumerate(data):
        substance_data.append({'id': i + 1, 'name': item['name'].lower(), 'symbol': item['symbol']})

        for k in ['mp', 'bp', 'hf', 'hv']:
            if item[k]:
                if k in ['mp', 'bp']:
                    item[k] = float(item[k])
                else:
                    item[k] = int(item[k])

        heat_data.append({"substance_id": i + 1,
                          "melting_point": item['mp'],
                          "boiling_point": item['bp'],
                          "heat_of_fusion": item['hf'],
                          "heat_of_vaporization": item['hv']})

    # Write to files
    with open('fixtures/substances.json', 'w') as f:
        f.write(json.dumps(substance_data))

    with open('fixtures/latent_heats.json', 'w') as f:
        f.write(json.dumps(heat_data))


def _element_fixtures():
    '''Create the element fixtures'''
    with open('fixtures/element_data.txt') as f:
        lines = f.readlines()
        data = []
        for line in lines:
            item = {}
            item['molecular_weight'], item['name'], item['symbol'], item['atomic_number'], item['group'] = [x.strip() for x in line.split(',')]
            data.append(item)

    with open('fixtures/elements.json', 'w') as f:
        f.write(json.dumps(data))


def create_fixtures():
    '''Create fixtures from comma-separated data'''
    _heat_fixtures()
    _element_fixtures()


def load_fixtures():
    '''Load initial database data'''
    # Import here, to avoid circular imports
    import models

    def load_fixture(filename, model):
        with open(filename) as f:
            data = f.read()
            data = json.loads(data)
            for item in data:
                db_session.add(model(**item))
            db_session.commit()

    load_fixture('fixtures/substances.json', models.Substance)
    load_fixture('fixtures/latent_heats.json', models.LatentHeats)
    load_fixture('fixtures/elements.json', models.Element)


def init_db():
    '''Initialize database with schema from models'''
    # import all modules here that define models
    import models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    '''Initialize database and data'''
    init_db()
    load_fixtures()
