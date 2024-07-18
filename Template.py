import streamlit as st
import requests
import pydeck as pdk
import pandas as pd

api_key = "1df68b90-936c-441d-89a9-997c23f61dfa"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

def display_weather_and_air_quality(data):
    location = data["city"]
    weather = data["current"]["weather"]
    pollution = data["current"]["pollution"]

    st.write("#### Weather", unsafe_allow_html=True)
    st.write(f"**Temperature (C):** {weather['tp']}°C")
    st.write(f"**Temperature (F):** {weather['tp'] * 9/5 + 32}°F")
    st.write(f"**Humidity:** {weather['hu']}%")
    st.write(f"**Wind Speed:** {weather['ws']} m/s")

    st.write("#### Air Quality", unsafe_allow_html=True)
    st.write(f"**AQI US:** {pollution['aqius']}")
    st.write(f"**Main Pollutant:** {pollution['mainus']}")

def display_map(latitude, longitude):
    # Create a DataFrame for pydeck
    df = pd.DataFrame({
        'latitude': [latitude],
        'longitude': [longitude]
    })

    # Create and display the map using pydeck
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/satellite-streets-v11',
            initial_view_state=pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[26, 255, 0, 160]',
                    get_radius=1000,
                    pickable=True,
                ),
            ],
            tooltip={
                "html": "Lat: {latitude} <br/> Long:{longitude}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }
        )
    )

# Category selection
category = st.selectbox(
    "Select the method to find air quality information:",
    ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"]
)

if category == "By City, State, and Country":
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    
    if countries_dict["status"] == "success":
        countries_list = [i["country"] for i in countries_dict["data"]]
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", options=countries_list)
        if country_selected:
            states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
            states_dict = requests.get(states_url).json()
            
            if states_dict["status"] == "success":
                states_list = [i["state"] for i in states_dict["data"]]
                states_list.insert(0, "")

                state_selected = st.selectbox("Select a state:", options=states_list)
                if state_selected:
                    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
                    cities_dict = requests.get(cities_url).json()
                    
                    if cities_dict["status"] == "success":
                        cities_list = [i["city"] for i in cities_dict["data"]]
                        cities_list.insert(0, "")

                        city_selected = st.selectbox("Select a city:", options=cities_list)
                        if city_selected:
                            aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                            aqi_data_dict = requests.get(aqi_data_url).json()

                            if aqi_data_dict["status"] == "success":
                                data = aqi_data_dict["data"]
                                display_weather_and_air_quality(data)
                                display_map(data["location"]["lat"], data["location"]["lon"])
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
        data = aqi_data_dict["data"]
        display_weather_and_air_quality(data)
        display_map(data["location"]["lat"], data["location"]["lon"])
    else:
        st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":
    latitude = st.text_input("Enter latitude:")
    longitude = st.text_input("Enter longitude:")
    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":
            data = aqi_data_dict["data"]
            display_weather_and_air_quality(data)
            display_map(data["location"]["lat"], data["location"]["lon"])
        else:
            st.warning("No data available for this location.")
