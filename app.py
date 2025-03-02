

# importing necessary libraries

import streamlit as st
import google.generativeai as genai
import requests
import datetime


# Setting up the API keys

GEMINI_API_KEY = st.secrets["api_keys"]["gemini"]
WEATHER_API_KEY = st.secrets["api_keys"]["weather"]


# Configuring and initialising gemini

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.0-flash-exp")

# Function to get itinerary suggestions
def generate_itinerary(destination,num_days,budget):
    
    response = model.generate_content(f"Suggest a basic {num_days}-day travel plan for {destination} with respect to the budget {budget}$.If the budget given is impractical, Give the plan according to the minimum possible practical budget. In the end, give a simple tabular summary of the plan and the estimated costs")
    return response.text if response else "No suggestions available."




# Function to get weather forecast (Using OpenWeatherMap API)
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    
    if response.get("main"):
        temp = response["main"]["temp"]
        weather_desc = response["weather"][0]["description"].capitalize()
        return f"🌡 Temperature: {temp}°C | 🌤 Condition: {weather_desc}", temp
    return "Weather data unavailable.", None



def recommend_clothing(temp, num_days):
    if temp is None:
        return "No recommendation available."
    
    if num_days < 3:
        if temp < 10:
            return "🧥 Wear a heavy jacket, gloves, and warm clothes."
        elif 10 <= temp < 20:
            return "👕 Light sweater or jacket recommended."
        else:
            return "🩳 T-shirt and light clothing are good."
    else:
        if temp < 10:
            return "🧥 Pack heavy jackets, gloves, and layers for warmth."
        elif 10 <= temp < 20:
            return "👕 Bring sweaters and jackets for varying temperatures."
        else:
            return "🩳 Pack T-shirts, shorts, and light clothing for comfort."




st.title("✈️ Travel Planner App")
st.sidebar.header("Plan Your Trip")

# User Inputs
source = st.sidebar.text_input("Enter Source Location", placeholder="E.g., New York, London")
destination = st.sidebar.text_input("Enter Destination", placeholder="E.g., Paris, New York")
start_date = st.sidebar.date_input("Start Date", datetime.date.today())
end_date = st.sidebar.date_input("End Date", datetime.date.today() + datetime.timedelta(days=3))
budget = st.sidebar.number_input("Enter Your Budget ($)", min_value=100, step=50)

# Calculate number of days
num_days = (end_date - start_date).days

# Display Travel Plan
if st.sidebar.button("🎒Start Planning"):
    if destination:
        st.subheader(f"🌍 Travel Plan for {destination}")
    
    
         # Itinerary (Sample itinerary for demonstration)
        st.subheader("Suggested plan for you")
        st.write(generate_itinerary(destination,num_days,budget))
        


        # Weather Forecast
        st.subheader("Weather Info")
        weather_info, temp = get_weather(destination)
        st.write(weather_info)
    
         # Clothing Recommendations
        st.subheader("👕 Recommended Clothing")
        st.write(recommend_clothing(temp, num_days))
    
    
    
    
