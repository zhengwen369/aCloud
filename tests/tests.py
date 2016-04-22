#  -*- coding: utf-8 -*-
import unittest
from web.frame import app, db


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        self.app = app.test_client()
        # db.create_all()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_t1(self):
        t1 = 1
        expected = 1
        assert t1 == expected

if __name__ == '__main__':
    unittest.main()