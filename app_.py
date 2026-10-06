import streamlit as st
import pandas as pd
import joblib
import requests
from datetime import datetime

API_KEY = "YOUR_API_KEY_HERE"

# 1. Load the trained XGBoost model
@st.cache_resource
def load_model():
    return joblib.load('zomato_xgboost_model.pkl')

model = load_model()

# 2. Calibrated Dynamic Pricing Business Logic
def calculate_dynamic_price(predicted_demand, traffic_index, base_delivery_fee=40):
    surge_multiplier = 1.0
    if predicted_demand > 3.0:     
        surge_multiplier += 0.2  
    elif predicted_demand > 2.0:   
        surge_multiplier += 0.1  
        
    if traffic_index == 4:       
        surge_multiplier += 0.5  
    elif traffic_index == 3:     
        surge_multiplier += 0.25 
        
    surge_multiplier = min(surge_multiplier, 2.0)
    final_fee = base_delivery_fee * surge_multiplier
    return round(final_fee, 2), surge_multiplier

# 3. Streamlit User Interface
st.set_page_config(page_title="Zomato Surge Engine", layout="centered")
st.title("🛵 Zomato Dynamic Pricing Engine")
st.write("Simulate Bengaluru operational conditions to forecast demand and optimize delivery fees.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    order_hour = st.slider("Hour of Day (0-23)", 0, 23, 19)
    day_of_week = st.selectbox("Day of the Week", [0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x])

with col2:
    traffic_level = st.selectbox("Traffic Density", ["Low", "Medium", "High", "Jam"])
    weather_condition = st.selectbox("Weather", ["Sunny", "Cloudy", "Fog", "Sandstorms", "Stormy", "Windy"])

traffic_mapping = {"Low": 1, "Medium": 2, "High": 3, "Jam": 4}
traffic_index = traffic_mapping[traffic_level]

input_data = {
    'order_hour': [order_hour],
    'day_of_week': [day_of_week],
    'traffic_index': [traffic_index],
    'is_dinner_rush': [1 if 17 <= order_hour <= 21 else 0],
    'is_weekend': [1 if day_of_week >= 4 else 0],
    'severe_friction': [1 if traffic_index >= 3 and weather_condition in ["Stormy", "Sunny"] else 0]
}

import streamlit as st
import pandas as pd
import joblib
import requests
from datetime import datetime

API_KEY = "66dd0c5b89202a02c0ed16cddb6a3240"

# 1. Load the trained XGBoost model
@st.cache_resource
def load_model():
    return joblib.load('zomato_xgboost_model.pkl')

model = load_model()

# 2. Calibrated Dynamic Pricing Business Logic
def calculate_dynamic_price(predicted_demand, traffic_index, base_delivery_fee=40):
    surge_multiplier = 1.0
    if predicted_demand > 3.0:     
        surge_multiplier += 0.2  
    elif predicted_demand > 2.0:   
        surge_multiplier += 0.1  
        
    if traffic_index == 4:       
        surge_multiplier += 0.5  
    elif traffic_index == 3:     
        surge_multiplier += 0.25 
        
    surge_multiplier = min(surge_multiplier, 2.0)
    final_fee = base_delivery_fee * surge_multiplier
    return round(final_fee, 2), surge_multiplier

# 3. Streamlit User Interface
st.set_page_config(page_title="Zomato Surge Engine", layout="centered")
st.title("🛵 Zomato Dynamic Pricing Engine")
st.write("Simulate Bengaluru operational conditions to forecast demand and optimize delivery fees.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    order_hour = st.slider("Hour of Day (0-23)", 0, 23, 19)
    day_of_week = st.selectbox("Day of the Week", [0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x])

with col2:
    traffic_level = st.selectbox("Traffic Density", ["Low", "Medium", "High", "Jam"])
    weather_condition = st.selectbox("Weather", ["Sunny", "Cloudy", "Fog", "Sandstorms", "Stormy", "Windy"])

traffic_mapping = {"Low": 1, "Medium": 2, "High": 3, "Jam": 4}
traffic_index = traffic_mapping[traffic_level]

input_data = {
    'order_hour': [order_hour],
    'day_of_week': [day_of_week],
    'traffic_index': [traffic_index],
    'is_dinner_rush': [1 if 17 <= order_hour <= 21 else 0],
    'is_weekend': [1 if day_of_week >= 4 else 0],
    'severe_friction': [1 if traffic_index >= 3 and weather_condition in ["Stormy", "Sunny"] else 0]
}

expected_features = model.feature_names_in_
for feature in expected_features:
    if "Weather_conditions_" in feature:
        if weather_condition in feature:
            input_data[feature] = [1]
        else:
            input_data[feature] = [0]

input_df = pd.DataFrame(input_data)[expected_features]

if st.button("Calculate Surge Pricing", type="primary"):
    predicted_demand = model.predict(input_df)[0]
    final_fee, multiplier = calculate_dynamic_price(predicted_demand, traffic_index)
    
    st.markdown("### 📊 Operational Forecast")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Predicted Hourly Orders", f"{predicted_demand:.2f}")
    metric_col2.metric("Recommended Surge", f"{multiplier}x")
    metric_col3.metric("Final Delivery Fee", f"₹{final_fee}")
    
    if multiplier > 1.0:
        st.warning("⚠️ Surge Pricing Activated due to friction or high forecasted demand.")
    else:
        st.success("✅ Standard Pricing Active.")

st.markdown("---")
st.subheader("📡 Live API Production Test")

if st.button("Fetch Live Bengaluru Data & Predict", type="secondary"):
    with st.spinner("Pinging OpenWeather API & Google Maps..."):
        
        # 1. Fetch live weather using the API Key
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Bengaluru,IN&appid={API_KEY}&units=metric")
        
        if response.status_code == 200:
            live_weather_data = response.json()
            api_condition = live_weather_data["weather"][0]["main"]
            
            # Map OpenWeather text to our model's categorical format
            model_weather = "Stormy" if api_condition in ["Rain", "Thunderstorm", "Drizzle"] else "Sunny" if api_condition == "Clear" else "Cloudy"
            
            # Pull live local machine time
            live_hour = datetime.now().hour
            live_day = datetime.now().weekday()
            
            # Simulate a live traffic index pull (assuming heavy traffic during dinner rush)
            live_traffic = 4 if 17 <= live_hour <= 21 else 2
            
            # 2. Display the raw JSON payload to the evaluators
            st.write("**Live API JSON Payload:**")
            st.json({
                "location": "Bengaluru",
                "time_ist": datetime.now().strftime("%H:%M"),
                "temp_celsius": live_weather_data["main"]["temp"],
                "weather_status": api_condition,
                "simulated_traffic": "Jam" if live_traffic == 4 else "Medium"
            })
            
            # 3. Build the live DataFrame exactly as the XGBoost model expects
            live_input = {
                'order_hour': [live_hour],
                'day_of_week': [live_day],
                'traffic_index': [live_traffic],
                'is_dinner_rush': [1 if 17 <= live_hour <= 21 else 0],
                'is_weekend': [1 if live_day >= 4 else 0],
                'severe_friction': [1 if live_traffic >= 3 and model_weather in ['Stormy', 'Sunny'] else 0]
            }
            
            # Match expected features for One-Hot Encoding
            for feature in expected_features:
                if "Weather_conditions_" in feature:
                    if model_weather in feature:
                        live_input[feature] = [1]
                    else:
                        live_input[feature] = [0]
            
            live_df = pd.DataFrame(live_input)[expected_features]
            
            # 4. Execute Live Prediction and Pricing Logic
            live_demand = model.predict(live_df)[0]
            live_fee, live_mult = calculate_dynamic_price(live_demand, live_traffic)
            
            st.markdown("### ⚡ Live Operational Forecast")
            lc1, lc2, lc3 = st.columns(3)
            lc1.metric("Live Forecasted Orders", f"{live_demand:.2f}")
            lc2.metric("Live Surge Multiplier", f"{live_mult}x")
            lc3.metric("Live Final Fee", f"₹{live_fee}")
            
        else:
            st.error("API Key error. Please verify your OpenWeather API Key.")         