#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""



import pandas as pd
import plotly.express as px
import json
import plotly

import warnings

import logging



class DataAnalyzer:
    def __init__(self, df, state='Illinois'):
        self.df = df
        self.state = state
        
        self.logger = logging.getLogger(__name__)
        
        self.county = ""

    def filter_and_prepare_data(self):
        # Filter DataFrame based on state
        
        #print("\n\n\n")
        #print("DataAnalyzer ... df info:")
        #print(self.df.columns)
        #print(self.df)
        #print(len(self.df))
        
        filtered_df = self.df[self.df['wwtp_jurisdiction'] == self.state].copy()
        
        #print("\n\n\n")
        #print("DataAnalyzer ... df info:")
        #print(filtered_df.columns)
        #print(filtered_df)
        #print(len(filtered_df))
        
        var_new_df = filtered_df.copy()
        
        var_new_df = var_new_df.groupby('county_names').first().reset_index()
        
        first_row_country_name = var_new_df.iloc[0]['county_names']
        
        self.county = first_row_country_name
        
        #self.logger.info("first_row_country_name = ")
        #self.logger.info(first_row_country_name)
        
        # pick first county here as some states have multiple counties:
        filtered_df = filtered_df[filtered_df["county_names"] == first_row_country_name]
        
        filtered_df_subset = filtered_df[['date_start', 'ptc_15d']]
        
        #print("\n\n\n")
        #print("DataAnalyzer ... df info:")
        #print(filtered_df_subset.columns)
        #print(filtered_df_subset)
        #print(len(filtered_df_subset))

        # Convert 'ptc_15d' to numeric and filter
        #filtered_df_subset['ptc_15d'] = pd.to_numeric(filtered_df_subset['ptc_15d'], errors='coerce')
        filtered_df_subset.loc[:, 'ptc_15d'] = pd.to_numeric(filtered_df_subset['ptc_15d'], errors='coerce')

        
        filtered_df_subset = filtered_df_subset[filtered_df_subset['ptc_15d'] <= 10000]

        # Clean and format DataFrame
        filtered_df_subset.dropna(inplace=True)
        filtered_df_subset.reset_index(drop=True, inplace=True)
        filtered_df_subset['date_start'] = pd.to_datetime(filtered_df_subset['date_start'])

        return filtered_df_subset

    def generate_visualization(self):
        # Prepare data for visualization
        filtered_df_subset = self.filter_and_prepare_data()

        # Generate Plotly figure
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)  
            title = f"{self.state} SARS-CoV-2 RNA Levels Over Time"
            fig = px.line(filtered_df_subset, x='date_start', y='ptc_15d', title=title)
            fig.update_layout(xaxis_title='Month', yaxis_title='% Change RNA levels over 15-day period')
            fig.update_xaxes(dtick="M1", tickformat='%b %Y', ticklabelmode="period", tickangle=45)
    
            # Convert Plotly figure to JSON
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON


