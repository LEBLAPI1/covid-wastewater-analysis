#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""

import sys
import os

# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from DataCollector.Data_Collector_with_REST_API import DataCollector

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        # Setup a test database URL
        #  production name:  DataCollector('sqlite:///ApiData.sqlite3')
        self.collector = DataCollector('sqlite:///:ApiData_TEST.sqlite3:')

    def test_init_db(self):
        # Test if the database initializes correctly
        self.collector.init_db()
        # Assert that tables are created, etc.

    def test_fetch_data_from_api(self):
        # Test the API fetching functionality
        data = self.collector.fetch_data_from_api()
        self.assertIsNotNone(data)
        # Further assertions based on expected data structure
       
    def test_store_data(self):
        # Mock data resembling the data structure from your table
        mock_data = [
            {
                'id': 1,
                'wwtp_jurisdiction': 'Illinois',
                'wwtp_id': '652',
                'reporting_jurisdiction': 'Illinois',
                'sample_location': 'Treatment plant',
                'key_plot_id': 'NWSS_il_652_Treatment plant_raw wastewater',
                'county_names': 'Shelby',
                'county_fips': '17173',
                'population_served': 5329,
                'date_start': '2022-02-01',
                'date_end': '2022-02-15',
                'detect_prop_15d': '100',
                'percentile': '51.0',
                'sampling_prior': 'no',
                'first_sample_date': '2022-02-15'
            },
            {
                'id': 2,
                'wwtp_jurisdiction': 'Illinois',
                'wwtp_id': '652',
                'reporting_jurisdiction': 'Illinois',
                'sample_location': 'Treatment plant',
                'key_plot_id': 'NWSS_il_652_Treatment plant_raw wastewater',
                'county_names': 'Shelby',
                'county_fips': '17173',
                'population_served': 5329,
                'date_start': '2022-02-02',
                'date_end': '2022-02-16',
                'detect_prop_15d': '100',
                'percentile': '43.5',
                'sampling_prior': 'no',
                'first_sample_date': '2022-02-15'
            },

        ]
    
        # Use store_data to save mock data
        self.collector.store_data(mock_data)
    
        # Add assertions to verify that the data is stored correctly
        # Example: Check if the record count matches, specific data fields are correct, etc.
        

        # Query the database to check if record with id 1 exists
        record_with_id_1 = self.collector.db_session.query(self.collector.ApiData).filter_by(id=1).first()
        self.assertIsNotNone(record_with_id_1, "Record with id 1 should exist in the database")
    
        # Query the database to check if record with id 2 exists
        record_with_id_2 = self.collector.db_session.query(self.collector.ApiData).filter_by(id=2).first()
        self.assertIsNotNone(record_with_id_2, "Record with id 2 should exist in the database")
        
        # Count the number of records in the database
        db_record_count = self.collector.db_session.query(self.collector.ApiData).count()
    
        # Check if the record count in the database matches the number of records in mock data
        expected_record_count = len(mock_data)  # The number of records you inserted
        self.assertEqual(db_record_count, expected_record_count, "The number of records in the database should match the number of records inserted")



# Add more tests as required for other methods

if __name__ == '__main__':
    unittest.main()
