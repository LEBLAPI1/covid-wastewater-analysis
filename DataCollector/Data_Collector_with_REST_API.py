#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""

################################
# This script grabs data from the CDC web site, specifically COVID 19 levels in wastwater 
#  the script stores that data within a database table for processing later
#    this assignment is only for the part of the collector and the storage within the database


"""
Data Collector with REST API

This script is designed to fetch data from a specific REST API, parse the data, and then store it in a SQLite database using Flask and SQLAlchemy. The primary focus of the script is to interact with the CDC's API to retrieve environmental data related to water treatment plants and store this data for further analysis.

Features:
- Fetch data from CDC's REST API (https://data.cdc.gov/resource/2ew6-ywp6.json).
- Parse the JSON data received from the REST API.
- Dynamically create a SQLite database and a corresponding table to store the data if they don't exist.
- Map the JSON data to a SQLAlchemy model (`ApiData`) and insert the data into the database.

The `ApiData` model represents the structure of the database table, which includes columns for various attributes like jurisdiction, ID, reporting jurisdiction, sample location, and others, including several date fields.

The script uses Flask as the web framework and SQLAlchemy as the ORM (Object-Relational Mapping) tool. The script is designed to be run as a standalone application, initializing the database and fetching the data upon execution.

Dependencies:
- Flask
- Flask-SQLAlchemy
- Requests
- datetime

"""

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base  # Updated import


from datetime import datetime
import requests

import json
import pandas as pd

import warnings





class DataCollector:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
        
        class ApiData(self.Base):
            __tablename__ = 'api_data'
            id = Column(Integer, primary_key=True)
            wwtp_jurisdiction = Column(String)
            wwtp_id = Column(String)
            reporting_jurisdiction = Column(String)
            sample_location = Column(String)
            key_plot_id = Column(String)
            county_names = Column(String)
            county_fips = Column(String)
            population_served = Column(Integer)
            date_start = Column(Date)
            date_end = Column(Date)
            detect_prop_15d = Column(String)
            percentile = Column(String)
            sampling_prior = Column(String)
            first_sample_date = Column(Date)
            ptc_15d=Column(Integer)
            sample_location_specify=Column(String)
            
        self.ApiData = ApiData

    def init_db(self):
        
        self.Base.metadata.drop_all(bind=self.engine)
        
        self.Base.metadata.create_all(bind=self.engine)

    @staticmethod
    def parse_date(date_string):
        if date_string:
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=FutureWarning)            
                var_return_date_time = datetime.strptime(date_string, "%Y-%m-%d").date()
            
            return var_return_date_time
        return None



    def fetch_data_from_api(self):
        response = requests.get("https://data.cdc.gov/resource/2ew6-ywp6.json")
        if response.status_code == 200:
            data = response.json()
    
            # Save to JSON file for debugging
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
    
            # Convert to DataFrame and save to CSV file for debugging
            df = pd.DataFrame(data)
            df.to_csv('data.csv', index=False)
    
            return data            

        else:
            raise Exception(f"API request failed ..... response code = {response.status_code}")

    def store_data(self, api_data):
        for record in api_data:
            new_record = self.ApiData(
                
                ########################
                ### columns from data source:
                    
                #wwtp_jurisdiction,
                #wwtp_id,
                #reporting_jurisdiction,
                #sample_location,
                #key_plot_id,
                #county_names,
                #county_fips,
                #population_served,
                #date_start,date_end,
                #detect_prop_15d,
                #percentile,
                #sampling_prior,
                #first_sample_date,
                #ptc_15d,
                #sample_location_specify
                
                wwtp_jurisdiction=record.get('wwtp_jurisdiction'),
                wwtp_id=record.get('wwtp_id'),
                reporting_jurisdiction=record.get('reporting_jurisdiction'),
                sample_location=record.get('sample_location'),
                key_plot_id=record.get('key_plot_id'),
                county_names=record.get('county_names'),
                county_fips=record.get('county_fips'),
                population_served=record.get('population_served'),
                date_start=self.parse_date(record.get('date_start')),
                date_end=self.parse_date(record.get('date_end')),
                detect_prop_15d=record.get('detect_prop_15d'),
                percentile=record.get('percentile'),
                sampling_prior=record.get('sampling_prior'),
                first_sample_date=self.parse_date(record.get('first_sample_date')),
                
                ptc_15d=record.get('ptc_15d'),
                sample_location_specify=record.get('sample_location_specify')
            )
            self.db_session.add(new_record)
        self.db_session.commit()

    def close_session(self):
        self.db_session.remove()


if __name__ == "__main__":
    collector = DataCollector('sqlite:///ApiData.sqlite3')
    try:
        collector.init_db()
        api_data = collector.fetch_data_from_api()
        collector.store_data(api_data)
        print("Script completed successfully. Data stored in SQLite DB.")
    except Exception as e:
        print(f"Script failed: {e}")
    finally:
        collector.close_session()
