import streamlit as st
import pandas as pd
import requests

# Base URL for Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Product Store Sale Predictor")

# Section for online prediction
st.header("Online Prediction")

# Collect user input for property features
Product_Weight = st.number_input("Product Weight", min_value=0.00, max_value = 1000.00, value = 0.00)
Product_Sugar_Content = st.selectbox("Product_Sugar_Content", ["No Sugar","Low Sugar", "Regular"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area")
Product_MRP= st.number_input("Product_MRP")
Store_Size = st.selectbox("Store_Size", ["Entire home/apt", "Private room", "Shared room"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type", ["Entire home/apt", "Private room", "Shared room"])
Store_Type = st.selectbox("Store_Type", ["Entire home/apt", "Private room", "Shared room"])
Product_Id_char = st.selectbox("Product_Id_char", ["Entire home/apt", "Private room", "Shared room"])
Store_Age_Years = st.number_input("Store_Age_Years")
Product_Type_Category = st.selectbox("Product_Type_Category", ["Entire home/apt", "Private room", "Shared room"])

# Convert user input into a DataFrame
input_data = pd.DataFrame(
    [
        {
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type
    'Store_Type': Store_Type,
    'Product_Id_char': Product_Id_char,
    'Store_Age_Years': Store_Age_Years,
    'Product_Type_Category': Product_Type_Category
}
        ]
    )
# Create a button to trigger the prediction
if st.button("Predict", type = "primary"):
  response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient="records")[0]) # Send data to Flask API

  if response.status_code == 200:
    st.success(f"Predicted Sale Price: {response.json()['Predicted Price (in dollars)']}")
  else:
    st.error(f"Error: {response.status_code}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

