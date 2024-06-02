from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV data into a DataFrame
df_summer = pd.read_csv('city_temp_summer.csv')
df_winter = pd.read_csv('city_temp_winter.csv')
@app.route('/temperature/summer', methods=['GET'])
def get_temperature_summer():
    country = request.args.get('country').lower()
    city = request.args.get('city').lower()

    # Filter the DataFrame based on the query parameters
    filtered_data = df_summer[(df_summer['Country'].str.lower() == country) & (df_summer['City'].str.lower() == city)]
    
    # Create the response in the desired format
    response = filtered_data[['year', 'averageTemperature']].rename(columns={'averageTemperature': 'temperature'}).to_dict(orient='records')

    return jsonify(response)

@app.route('/temperature/winter', methods=['GET'])
def get_temperature_winter():
    country = request.args.get('country').lower()
    city = request.args.get('city').lower()

    # Filter the DataFrame based on the query parameters
    filtered_data = df_winter[(df_winter['Country'].str.lower() == country) & (df_winter['City'].str.lower() == city)]
    
    # Create the response in the desired format
    response = filtered_data[['year', 'averageTemperature']].rename(columns={'averageTemperature': 'temperature'}).to_dict(orient='records')

    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
