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

    #data = data_collector.ApiData.query.filter_by(wwtp_jurisdiction=state).all()
    #df = pd.DataFrame([item.__dict__ for item in data])
    
    df = data_collector.df_data.copy()
    #app.logger.info(f"DataFrame columns: {df.columns}")
    #app.logger.info(f"DataFrame columns: {df}")
    df = df[df["wwtp_jurisdiction"]==state]
    
    #print("from app.py df output here:")
    #print(df.columns)
    #app.logger.info(f"DataFrame columns: {df.columns}")
    #app.logger.info(f"DataFrame columns: {df}")

    # Create an instance of DataAnalyzer
    data_analyzer = DataAnalyzer(df, state)

    # Generate visualization
    graphJSON = data_analyzer.generate_visualization()
    
    var_county_name = data_analyzer.county

    #return jsonify({'graphJSON': graphJSON})
    return jsonify({'graphJSON': graphJSON, 'countyName': var_county_name})


if __name__ == '__main__':
    
    # first run the unit tests:
    # this code finds all the test files within the UnitTest sub directory:
    unittest.TextTestRunner().run(unittest.TestLoader().discover('UnitTests'))
       
    print("Starting Flask app")
    #app.run(host='192.168.0.60', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='localhost', port=5000, debug=True)
    
    


