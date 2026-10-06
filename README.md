# 🛵 Zomato Dynamic Pricing Engine (Bengaluru Operations)

An end-to-end predictive logistics and real-time dynamic surge pricing engine built with XGBoost and Streamlit. The system predicts hyper-local delivery demand surges across Bengaluru by ingesting live environmental and traffic friction signals.

---

## 📌 Project Overview
* **Objective:** Mitigate fleet shortages and order cancellations during high-friction operating conditions (rush hour, monsoon rains, severe traffic jams) by dynamically calibrating delivery fees.
* **Core Technology:** Python, XGBoost Regressor (`count:poisson`), Streamlit, Requests.
* **Production Integrations:** Real-time OpenWeatherMap API and TomTom Routing API for live environmental signals.

---

## 📈 Model Performance
* **Objective Function:** `count:poisson` (Optimized for discrete count distributions)
* **Mean Absolute Error (MAE):** `0.70 orders`
* **Root Mean Squared Error (RMSE):** `0.91 orders`
* **Key Engineered Features:** `is_dinner_rush`, `is_weekend`, `severe_friction`

---

## ⚙️ Architecture & Pipeline
1. **Live Ingestion:** Fetches real-time weather conditions for Bengaluru via OpenWeatherMap and travel delay ratios between major arterial hubs (Electronic City ➔ Silk Board) via TomTom.
2. **Feature Transformation:** Parses nested JSON responses into tabular feature vectors matching the model schema.
3. **Inference & Pricing Engine:** XGBoost outputs hourly demand forecasts, dynamically adjusting base delivery fees from 1.0x up to a 2.0x surge cap.

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/hebbarsudeep-collab/zomato-dynamic-pricing-engine.git](https://github.com/hebbarsudeep-collab/zomato-dynamic-pricing-engine.git)
   cd zomato-dynamic-pricing-engine
