import os

import unittest 
from fastfood import db
import ujson as json
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.session = db.session()

    def tearDown(self):
        # Deletes the contents for all the tables in reverse order, so the children
        # are deleted first
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def load_json_resource(self, name):
        with open('tests/resources/%s' % name) as _f:
            return self.json_to_dict(_f.read())

    def json_to_dict(self, json_str):
        return json.loads(json_str)

    def get_response_json(self, *args, **kwargs):
        status_code = kwargs.pop('status_code', 200)
        response = self.client.get(*args, **kwargs)
        self.assertStatus(response, status_code)
        return self.json_to_dict(response.data)

    def make_url(self, base, **kwargs):
        base += '?'
        params = map(lambda key: "%s=%s" % (str(key[0]), str(key[1])), kwargs.items())
        base += '&'.join(params)
        return base
