from flask import Flask, render_template, jsonify, request
import pandas as pd


# Import the DataCollector class
from DataCollector.Data_Collector_with_REST_API import DataCollector
from DataAnalyzer.DataAnalyzer import DataAnalyzer
import unittest

app = Flask(__name__)

# Create an instance of DataCollector
data_collector = DataCollector('sqlite:///ApiData.sqlite3')

# Initialize the database (create tables)
data_collector.init_db()

# Optionally, fetch and store data
api_data = data_collector.fetch_data_from_api()
data_collector.store_data(api_data)


# you might need to update the local host below for your machine:  app.run(host='192.168.0.60', port=5000, debug=True)

# try 1, testing another change / commit here for CI / CD pipeline on GitHub

# try 2, testing another change / commit here for CI / CD pipeline on GitHub


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Removed app.app_context() as it is not necessary here
    data = data_collector.ApiData.query.limit(100).all()  # Get the first 100 records
    data_dicts = [item.__dict__ for item in data]
    for record in data_dicts:
        record.pop('_sa_instance_state', None)  # Remove SQLAlchemy instance state
    return jsonify(data_dicts)

@app.route('/dropdown-data')
def dropdown_data():
    data = data_collector.ApiData.query.all()

    df = pd.DataFrame([item.__dict__ for item in data])

    unique_states = df['wwtp_jurisdiction'].unique().tolist()

    return jsonify({'states': unique_states})

@app.route('/show-visualization')
def show_visualization():
    return render_template('visualization.html')


@app.route('/visualization')
def visualize_data():
    state = request.args.get('state', "Illinois")  # Default to Illinois if not specified

    # Removed app.app_context() here as well
    data = data_collector.ApiData.query.filter_by(wwtp_jurisdiction=state).all()
    df = pd.DataFrame([item.__dict__ for item in data])

    # Create an instance of DataAnalyzer
    data_analyzer = DataAnalyzer(df, state)

    # Generate visualization
    graphJSON = data_analyzer.generate_visualization()

    return jsonify({'graphJSON': graphJSON})


if __name__ == '__main__':
    
    # first run the unit tests:
    # this code finds all the test files within the UnitTest sub directory:
    unittest.TextTestRunner().run(unittest.TestLoader().discover('UnitTests'))
       
    print("Starting Flask app")
    app.run(host='192.168.0.60', port=5000, debug=True)
    


