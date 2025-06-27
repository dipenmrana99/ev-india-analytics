import sqlite3
import pandas as pd
import folium
from geopy.geocoders import Nominatim
import time
import webbrowser
import os

# Load cached coordinates if exists
try:
    cached_coords = pd.read_csv("cached_coords.csv")
except FileNotFoundError:
    cached_coords = pd.DataFrame(columns=["Place", "State", "Latitude", "Longitude"])

# Connect to your database and read data
conn = sqlite3.connect('ev_india.db')
df = pd.read_sql_query("SELECT * FROM EV_Maker_by_Place", conn)
conn.close()

# Merge with cached coordinates to skip re-geocoding
df = df.merge(cached_coords, on=["Place", "State"], how="left")

# Geocoder
geolocator = Nominatim(user_agent="ev_map_geocoder")

new_coords = []

for i, row in df.iterrows():
    if pd.isnull(row['Latitude']) or pd.isnull(row['Longitude']):
        location_str = f"{row['Place']}, {row['State']}, India"
        try:
            location = geolocator.geocode(location_str)
            if location:
                df.at[i, 'Latitude'] = location.latitude
                df.at[i, 'Longitude'] = location.longitude
                new_coords.append({
                    "Place": row['Place'],
                    "State": row['State'],
                    "Latitude": location.latitude,
                    "Longitude": location.longitude
                })
                print(f"Geocoded: {location_str}")
            else:
                print(f"Not found: {location_str}")
            time.sleep(1)  # still needed for new entries
        except Exception as e:
            print(f"Error: {location_str} => {e}")

# Update cache file with new geocodes
if new_coords:
    new_df = pd.DataFrame(new_coords)
    cached_coords = pd.concat([cached_coords, new_df], ignore_index=True).drop_duplicates()
    cached_coords.to_csv("cached_coords.csv", index=False)

# Create map
ev_map = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

# Plot markers
for _, row in df.dropna(subset=['Latitude', 'Longitude']).iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['EV Maker']}<br>{row['Place']}, {row['State']}",
        icon=folium.Icon(color='blue', icon='car', prefix='fa')
    ).add_to(ev_map)

# Show map
map_path = "ev_maker_map.html"
ev_map.save(map_path)
webbrowser.open('file://' + os.path.realpath(map_path))
