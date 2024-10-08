import os

import streamlit as st
import pandas as pd
from streamlit_folium import folium_static

from backend import *

# Streamlit app layout
st.title('Veluweloopen :runner:')

# Load GPX files for each user
gpx_folder = 'Lopersroute-Runnersroute-2024/'
user_files = list(pd.read_csv('Veluweloop.csv')['runner'])

if user_files:
    # Select user to view route
    user_selection = st.selectbox('Select a user to view their GPX route:', user_files)

    run_start_time, gpx_files = show_runner_data(user_selection)
    
    st.markdown("## Running start time:" + run_start_time)

    # Load selected user's GPX route
    files = []
    for gpx_file in gpx_files:
        selected_gpx = load_gpx(os.path.join(gpx_folder, gpx_file))
        files.append(selected_gpx)
    
    # Create map with the selected user's route
    gpx_map = create_map(files)
    
    # Display the map
    folium_static(gpx_map)
else:
    st.error("No GPX files found. Please add GPX files to the 'gpx/' folder.")
