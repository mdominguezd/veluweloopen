import os
import time

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import LocateControl

from backend import *

# Set page configuration
st.set_page_config(
    page_title="Veluweloopen",   # Title that appears in the browser tab
    page_icon=":runner:",                        # Custom emoji or image as the favicon
    initial_sidebar_state="collapsed"       # Can be "expanded", "collapsed", or "auto"
)

# Streamlit app layout
st.title('Veluweloopen :runner:')

# Load GPX files for each user
gpx_folder = 'Lopersroute-Runnersroute-2024/'
user_files = list(pd.read_csv('Veluweloop.csv')['runner'])

if user_files:
    # Select user to view route
    user_selection = st.selectbox('Select a user to view their GPX route:', user_files)

    run_start_time, gpx_files = show_runner_data(user_selection)

    st.markdown("<h1 style='text-align: center'> &#128336 </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center'>Running start time: " + run_start_time + "</h2>", unsafe_allow_html=True)

    go_start_point = st.toggle("Take me to the starting point")

    # Load selected user's GPX route
    files = []
    for gpx_file in gpx_files:
        selected_gpx = load_gpx(os.path.join(gpx_folder, gpx_file))
        files.append(selected_gpx)
    
    # Create map with the selected user's route
    gpx_map = create_map(files)

    if go_start_point:

        LocateControl(auto_start=True,
                    ).add_to(gpx_map)        
        m = st_folium(gpx_map, width = 1, height = 1)

        # Check if `current_location` is already in session_state
        if 'current_location' not in st.session_state:
            time.sleep(2)
            # Store the first current_location from the map in session_state
            st.session_state['current_location'] = [m['center']['lng'], m['center']['lat']]

        current_location = st.session_state['current_location']
        gpx_map = get_to_start(gpx_map, current_location, [files[0][0][1], files[0][0][0]])

        m = st_folium(gpx_map, width = '100%')
    else:
        # Display the map
        m = st_folium(gpx_map, width = '100%')
else:
    st.error("No GPX files found. Please add GPX files to the 'gpx/' folder.")
