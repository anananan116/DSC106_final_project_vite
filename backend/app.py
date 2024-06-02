from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV data into a DataFrame
df_summer = pd.read_csv('temperature_data.csv')
df_winter = pd.read_csv('temperature_data.csv')
@app.route('/temperature/summer', methods=['GET'])
def get_temperature():
    country = request.args.get('country').lower()
    city = request.args.get('city').lower()

    # Filter the DataFrame based on the query parameters
    filtered_data = df_summer[(df_summer['country'].str.lower() == country) & (df_summer['city'].str.lower() == city)]
    
    # Create the response in the desired format
    response = filtered_data[['year', 'averageTemperature']].rename(columns={'averageTemperature': 'temperature'}).to_dict(orient='records')

    return jsonify(response)

@app.route('/temperature/winter', methods=['GET'])
def get_temperature():
    country = request.args.get('country').lower()
    city = request.args.get('city').lower()

    # Filter the DataFrame based on the query parameters
    filtered_data = df_winter[(df_winter['country'].str.lower() == country) & (df_winter['city'].str.lower() == city)]
    
    # Create the response in the desired format
    response = filtered_data[['year', 'averageTemperature']].rename(columns={'averageTemperature': 'temperature'}).to_dict(orient='records')

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
