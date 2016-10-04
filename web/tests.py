import os
import json
from app import app
from database import init_db, load_fixtures
import unittest
import tempfile


class WebTestCase(unittest.TestCase):
    '''Test web setup'''
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
        rv = self.app.get('/latent_heats/')
        data = json.loads(rv.data)['data']
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(data, [])


class LatentHeatAPITestCase(unittest.TestCase):
    '''Test the LatentHeat API endpoints'''
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

    def test_get_latent_heats_detail(self):
        rv = self.app.get('/latent_heats/10/')
        data = json.loads(rv.data)['data']
        self.assertEqual(float(data['boiling_point']), 172.0)

    def test_get_latent_heats(self):
        rv = self.app.get('/latent_heats/')
        data = json.loads(rv.data)['data']
        self.assertGreater(len(data), 0)
        self.assertListEqual(data[0].keys(), [u'substance', u'boiling_point', u'heat_of_vaporization',
                                              u'substance_id', u'melting_point', u'heat_of_fusion'])

    def test_get_latent_heats_page(self):
        rv = self.app.get('/latent_heats/?page[limit]=10')
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 10)

    def test_get_latent_heats_filter_exact(self):
        rv = self.app.get('/latent_heats/?filter[boiling_point]=100.0')
        data = json.loads(rv.data)['data']
        self.assertGreater(len(data), 1)
        for item in data:
            self.assertEqual(float(item['boiling_point']), 100.0)

    def test_get_latent_heats_filter_gt(self):
        rv = self.app.get('/latent_heats/?filter[boiling_point__gt]=100.0')
        data = json.loads(rv.data)['data']
        self.assertGreater(len(data), 1)
        for item in data:
            self.assertGreater(float(item['boiling_point']), 100.0)

    def test_get_latent_heats_filter_lte(self):
        rv = self.app.get('/latent_heats/?filter[boiling_point__lte]=100.0')
        data = json.loads(rv.data)['data']
        self.assertGreater(len(data), 1)
        for item in data:
            self.assertLessEqual(float(item['boiling_point']), 100.0)

    def test_get_latent_heats_filter_relationship(self):
        rv = self.app.get('/latent_heats/?filter[substance__name]=water')
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['substance']['symbol'], 'H2O')


class SubstanceTestCase(unittest.TestCase):
    '''Test the Substance API endpoints'''

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

    def test_get_substances(self):
        rv = self.app.get('/substances/')
        data = json.loads(rv.data)['data']
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()
