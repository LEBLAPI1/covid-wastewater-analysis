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
        
        data = {
            'id': [1, 2],
            'wwtp_jurisdiction': ['Illinois', 'Illinois'],
            'wwtp_id': [652, 652],
            'reporting_jurisdiction': ['Illinois', 'Illinois'],
            'sample_location': ['Treatment plant', 'Treatment plant'],
            'key_plot_id': ['NWSS_il_652_Treatment plant_raw wastewater', 'NWSS_il_652_Treatment plant_raw wastewater'],
            'county_names': ['Shelby', 'Shelby'],
            'county_fips': [17173, 17173],
            'population_served': [5329, 5329],
            'date_start': ['2022-02-01', '2022-02-02'],
            'date_end': ['2022-02-15', '2022-02-16'],
            'detect_prop_15d': [100, 100],
            'percentile': [51.0, 43.5],
            'sampling_prior': ['no', 'no'],
            'first_sample_date': ['2022-02-15', '2022-02-15'],
            'ptc_15d': [100, 100]  # Added as an example
        }

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
