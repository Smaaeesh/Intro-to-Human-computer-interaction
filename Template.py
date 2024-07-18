import streamlit as st
import requests

api_key = "1df68b90-936c-441d-89a9-997c23f61dfa"

st.set_page_config(page_title="Weather and Air Quality Web App", page_icon="☁️")

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

@st.cache_data
def map_creator(latitude, longitude):
    from streamlit_folium import folium_static
    import folium

    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup="Location", tooltip="Location").add_to(m)
    folium_static(m)

@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    return countries_dict

@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    return states_dict

@st.cache_data
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    return cities_dict

# Sidebar for location selection method
category = st.sidebar.selectbox(
    "Select the method to find air quality information:",
    ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"]
)

def display_weather_and_air_quality(data):
    location = data["city"]
    weather = data["current"]["weather"]
    pollution = data["current"]["pollution"]
    latitude = data["location"]["coordinates"][1]
    longitude = data["location"]["coordinates"][0]

    temp_celsius = weather['tp']
    temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)

    st.write(f"### Air Quality and Weather Data for {location}")

    st.markdown(
        f"<div style='background-color: lightblue; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
        f"**Temperature:** {temp_celsius}°C / {temp_fahrenheit}°F"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style
