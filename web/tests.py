import os
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
        self.assertEqual(rv.status_code, 200)
        print rv.data


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
        print rv.response



if __name__ == '__main__':
    unittest.main()
