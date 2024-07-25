import streamlit as st
import requests
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

api_key = "sXEjCjQh3vCYZoGbQgEekBX9bmN1EVJRmVilK25JkdVprFEQ6foUwrbW0zTt"

# Configure the page
st.set_page_config(page_title="Sports Score Tracker", page_icon="🏆")

# Title and header
st.title("Sports Score Tracker")
st.header("Live Scores, Win Streaks, and More")

# Color picker for background
bg_color = st.color_picker("Choose Background Color", "#f0f0f0")
st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar for team selection
team_options = ["Team A", "Team B", "Team C"]  # Replace with your teams
selected_teams = st.multiselect("Select teams to track:", team_options)

# Function to fetch and display real-time scores
def fetch_scores():
    # Placeholder for API call to get scores
    url = f"https://api.sportmonks.com/v3/fixtures?api_token={api_key}"
    response = requests.get(url)
    scores = response.json()  # Replace with actual API response handling
    return scores

# Display real-time scores
if selected_teams:
    scores = fetch_scores()
    st.write("### Real-Time Scores")
    for team in selected_teams:
        st.write(f"Scores for {team}: {scores.get(team, 'No data available')}")

# Graph showing team’s win streak status
def plot_win_streak(team_name):
    # Placeholder for API call to get win streak data
    win_streaks = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=10),
        'Wins': [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]  # Example data
    })
    fig, ax = plt.subplots()
    ax.plot(win_streaks['Date'], win_streaks['Wins'], marker='o')
    ax.set_title(f"Win Streak for {team_name}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Wins')
    st.pyplot(fig)

if selected_teams:
    selected_team_for_streak = st.selectbox("Select a team to view win streak:", selected_teams)
    plot_win_streak(selected_team_for_streak)

# Map to locate local stadium
def plot_stadium_location(stadium_lat, stadium_lon):
    view_state = pdk.ViewState(
        latitude=stadium_lat,
        longitude=stadium_lon,
        zoom=12,
        pitch=50
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=[{"latitude": stadium_lat, "longitude": stadium_lon}],
        get_position='[longitude, latitude]',
        get_color='[255, 0, 0, 160]',
        get_radius=200,
        pickable=True,
    )

    tooltip = {
        "html": f"Stadium Location<br/>Lat: {stadium_lat} <br/> Long: {stadium_lon}",
        "style": {
            "backgroundColor": "darkblue",
            "color": "white"
        }
    }

    r = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v10',
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    )

    st.pydeck_chart(r)

# Example stadium coordinates (replace with actual coordinates)
stadium_lat = 40.4406
stadium_lon = -79.9959
plot_stadium_location(stadium_lat, stadium_lon)

# Email updates
email = st.text_input("Enter your email for regular updates:")
if st.button("Subscribe"):
    if email:
        st.success(f"Subscribed successfully with {email}")
        # Placeholder for email subscription logic
    else:
        st.warning("Please enter a valid email address.")
