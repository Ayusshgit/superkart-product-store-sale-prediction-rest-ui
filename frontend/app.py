import streamlit as st
import pandas as pd
import requests

# Base URL for Flask backend
# BACKEND_URL = "http://backend:7860"
BACKEND_URL = "http://172.18.0.1:7860"

# Set the title of the Streamlit app
st.title("SuperKart Product Store Sale Predictor")

# Section for online prediction
st.header("Online Prediction")

# Collect user input for property features
Product_Weight = st.number_input("Product Weight", min_value=0.00, max_value = 1000.00, value = 0.00)
Product_Sugar_Content = st.selectbox("Product_Sugar_Content", ["No Sugar","Low Sugar", "Regular"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area", min_value=0.001, max_value = 100.000, value = 0.001)
Product_MRP= st.number_input("Product_MRP", min_value=1.00, max_value = 1000.00, value = 1.00)
Store_Size = st.selectbox("Store_Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store_Type", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"])
Product_Id_char = st.selectbox("Product_Id_char", ["FD", "NC", "DR"])
Store_Age_Years = st.number_input("Store_Age_Years")
Product_Type_Category = st.selectbox("Product_Type_Category", ["Perishables", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame(
    [
        {
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Id_char': Product_Id_char,
    'Store_Age_Years': Store_Age_Years,
    'Product_Type_Category': Product_Type_Category
}
        ]
    )
# Create a button to trigger the prediction
if st.button("Predict", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=input_data.to_dict(orient="records")[0],
            timeout=30
        )

        if response.status_code == 200:
            prediction=response.json()['Predicted Price (in dollars)']
            st.success(f"Predicted Sale Price: {prediction}")
        else:
            st.error(f"Backend Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to backend: {e}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
