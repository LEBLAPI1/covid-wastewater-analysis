#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""

import sys
import os

# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Messenger import Messenger  

class TestServiceHealth(unittest.TestCase):
    
    def test_service_health(self):
        url = "http://192.168.0.60:5000/"
        messenger = Messenger(url)
        service_ok, message = messenger.check_service()
        self.assertTrue(service_ok, f"Service health check failed: {message}")

if __name__ == '__main__':
    unittest.main()
