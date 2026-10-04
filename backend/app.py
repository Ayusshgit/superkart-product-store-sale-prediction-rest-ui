# Import necessary libraries
import numpy as np
import os
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
store_sales_predictor_api = Flask("SuperKart Product Store Sale Predictor")

# load pre-trained machine learning model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "superKartModel_v1.joblib")
# model_path = "../superKartModel_v1.joblib"
model = joblib.load(model_path)

# Define a route for homepage (GET Request)
@store_sales_predictor_api.get('/')
def home():
  """
  This function handles GET requests to the root URL ('/').
  It returns a simple welcome message.
  """
  return "<h1>SuperKart Product Store Sale Predictor</h1>"

# Define a route for single product store prediction using POST request
@store_sales_predictor_api.post('/v1/predict')
def predict_single_product_store_sales():
  """
  This function handles POST requests to the '/v1/predict' endpoint.
  It expects a JSON payload containing property details and returns
  the predicted sale price as a JSON response.
    """
  # Get the JSON data from the request body
  property_data = request.get_json()

  # Extract relevant features from the JSON data
  sample = {
    'Product_Weight': property_data['Product_Weight'],
    'Product_Sugar_Content': property_data['Product_Sugar_Content'],
    'Product_Allocated_Area': property_data['Product_Allocated_Area'],
    'Product_MRP': property_data['Product_MRP'],
    'Store_Size': property_data['Store_Size'],
    'Store_Location_City_Type': property_data['Store_Location_City_Type'],
    'Store_Type': property_data['Store_Type'],
    'Product_Id_char': property_data['Product_Id_char'],
    'Store_Age_Years':property_data['Store_Age_Years'],
    'Product_Type_Category': property_data['Product_Type_Category']
    }
    
  # Convert the extracted data into a Pandas DataFrame
  input_data = pd.DataFrame([sample])

  # Make prediction
  predicted_price  = model.predict(input_data)[0]

  # Return the actual price
  return jsonify({'Predicted Price (in dollars)': predicted_price})

# Define a route for batch product store sales prediction using POST request
@store_sales_predictor_api.post('/v1/predictbatch')
def predict_batch_product_store_sales():
  """
  This function handles POST requests to the '/v1/predictbatch' endpoint.
  It expects a CSV file containing store and product details and returns
  the predicted sale price as a JSON response.
  """
  # Get the uploaded CSV file from the request
  file = request.files['file']

  # Read the CSV file into a Pandas DataFrame
  input_data = pd.read_csv(file)

  # Make predictions for all properties in the Dataframe
  predicted_prices = model.predict(input_data).tolist()

  return jsonify({'Predicted Prices (in dollars)': predicted_prices})

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    store_sales_predictor_api.run(host="0.0.0.0", port=7860, debug=True)
