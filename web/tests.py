import os
import json
from app import app
from database import init_db, load_fixtures
import unittest
import tempfile


class WebTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_get_empty(self):
        rv = self.app.get('/latent_heat')
        data = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(data, [])


class LatentHeatTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            init_db()
            load_fixtures()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_get_latent_heats(self):
        rv = self.app.get('/latent_heat')
        data = json.loads(rv.data)
        self.assertGreater(len(data), 0)
        self.assertListEqual(data[0].keys(), [u'substance',  u'boiling_point',
                                              u'heat_of_fusion',  u'heat_of_vaporization',
                                              u'melting_point', u'id'])


if __name__ == '__main__':
    unittest.main()
