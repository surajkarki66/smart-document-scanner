import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import url_for
from app import create_app

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_hello_world(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smart Scanner', response.data)

if __name__ == '__main__':
    unittest.main()
