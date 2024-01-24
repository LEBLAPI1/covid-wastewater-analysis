#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""

import sys
import os

# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from DataAnalyzer.DataAnalyzer import DataAnalyzer
import pandas as pd

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a mock DataFrame to test with
        data = {'wwtp_jurisdiction': ['Illinois', 'Illinois', 'Other'], 'ptc_15d': ['100', '200', '300'], 'date_start': ['2021-01-01', '2021-01-02', '2021-01-03']}
        self.df = pd.DataFrame(data)
        self.analyzer = DataAnalyzer(self.df, 'Illinois')

    def test_filter_and_prepare_data(self):
        # Test data filtering and preparation
        filtered_data = self.analyzer.filter_and_prepare_data()
        self.assertEqual(len(filtered_data), 2)  # Assuming only Illinois data is kept

    def test_generate_visualization(self):
        # Test visualization generation
        graphJSON = self.analyzer.generate_visualization()
        self.assertIsNotNone(graphJSON)

# Add more tests as required for other methods

if __name__ == '__main__':
    unittest.main()
