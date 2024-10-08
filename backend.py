import folium
import gpxpy
import pandas as pd
from folium.plugins import LocateControl

# Function to load GPX data
def load_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append([point.latitude, point.longitude])
        return points

# Function to create folium map with GPX route centered on the route's centroid
def create_map(gpx_routes):
    # Calculate the centroid of all points
    latitudes = []
    longitudes = []
    
    for route in gpx_routes:
        for point in route:
            latitudes.append(point[0])
            longitudes.append(point[1])
    
    # Calculate the centroid (average of latitudes and longitudes)
    centroid_lat = sum(latitudes) / len(latitudes)
    centroid_lon = sum(longitudes) / len(longitudes)
    
    # Create map centered on the centroid
    m = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=12)
    
    # Add LocateControl for current location
    LocateControl().add_to(m)

    # Color options for different routes
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple']
    
    # Add GPX routes to the map
    for i, route in enumerate(gpx_routes):
        if i == 0:
            # First route is for the runner (in red)
            folium.PolyLine(route, color='red', weight=2.5, opacity=1, tooltip="Runner").add_to(m)
        else:
            # Other routes are for cyclists
            folium.PolyLine(route, color=colors[i], weight=2.5, opacity=1, tooltip="Cyclist").add_to(m)
    
    # Add a custom legend (HTML)
    legend_html = '''
     <div style="position: fixed;
                 bottom: 50px; left: 50px; width: 150px; height: 90px; color: black;
                 background-color: white; border:2px black; z-index:9999; font-size:14px;
                 ">
     &nbsp;<b style='text-align: center'>Legend</b><br>
     &nbsp;<i style="color:red"> -- </i>&nbsp;Running<br>
     &nbsp;<i style="color:blue"> -- </i>&nbsp;Cycling
     </div>
     '''
    
    # Create a DivIcon for the legend
    legend_overlay = folium.DivIcon(html=legend_html)

     # Add the legend as an overlay
    folium.Marker([centroid_lat + 0.01, centroid_lon - 0.02], icon=legend_overlay).add_to(m)

    
    return m

def show_runner_data(runner):

    df = pd.read_csv('Veluweloop.csv')

    run_df = df[df['runner'] == runner]
    cycle_df = df[df['cyclist'] == runner]

    gpx_files = list(run_df['gpx_path']) + list(cycle_df['gpx_path'])

    run_start_time = run_df['start_time'].iloc[0]

    return run_start_time, gpx_files