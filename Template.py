import streamlit as st
import requests


api_key = "1df68b90-936c-441d-89a9-997c23f61dfa"

st.set_page_config(page_title="Weather and Air Quality Web App", page_icon="☁️")

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

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
        f"<div style='background-color: lightblue; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
        f"**Humidity:** {weather['hu']}%"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color: lightblue; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
        f"**Wind Speed:** {weather['ws']} m/s"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color: lightblue; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
        f"**AQI US:** {pollution['aqius']}"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color: lightblue; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
        f"**Main Pollutant:** {pollution['mainus']}"
        f"</div>",
        unsafe_allow_html=True
    )

    st.write(f"### Map for {location}")
    
    # Create and display the map using st_folium
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup="Location", tooltip="Location").add_to(m)
    st_folium(m, width=700, height=500)

if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = [i["country"] for i in countries_dict["data"]]
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", options=countries_list)
        if country_selected:
            states_dict = generate_list_of_states(country_selected)
            if states_dict["status"] == "success":
                states_list = [i["state"] for i in states_dict["data"]]
                states_list.insert(0, "")

                state_selected = st.selectbox("Select a state:", options=states_list)
                if state_selected:
                    cities_dict = generate_list_of_cities(state_selected, country_selected)
                    if cities_dict["status"] == "success":
                        cities_list = [i["city"] for i in cities_dict["data"]]
                        cities_list.insert(0, "")

                        city_selected = st.selectbox("Select a city:", options=cities_list)
                        if city_selected:
                            aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                            aqi_data_dict = requests.get(aqi_data_url).json()

                            if aqi_data_dict["status"] == "success":
                                display_weather_and_air_quality(aqi_data_dict["data"])
                            else:
                                st.warning("No data available for this location.")
                        else:
                            st.warning("Please select a city.")
                    else:
                        st.warning("No cities available, please select another state.")
            else:
                st.warning("No states available, please select another country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")

elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":
        display_weather_and_air_quality(aqi_data_dict["data"])
    else:
        st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":
    latitude = st.text_input("Enter latitude:")
    longitude = st.text_input("Enter longitude:")
    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":
            display_weather_and_air_quality(aqi_data_dict["data"])
        else:
            st.warning("No data available for this location.")
