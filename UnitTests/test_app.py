#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""

import sys
import os

# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_data_route(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        # Further assertions based on the response content

    # Add tests for other routes

if __name__ == '__main__':
    unittest.main()
