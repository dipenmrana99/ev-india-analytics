import sqlite3
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
import webbrowser, os

# Step 1: Load PCS data
conn = sqlite3.connect('ev_india.db')
pcs_df = pd.read_sql_query("SELECT * FROM OperationalPC", conn)
conn.close()

pcs_df.columns = ['state', 'pcs']
pcs_df['state'] = pcs_df['state'].str.lower().str.strip()

# Step 2: Load GeoJSON file
india = gpd.read_file("india_state_geo.json")
india['NAME_1'] = india['NAME_1'].str.lower().str.strip()

# Step 3: Merge data
merged = india.merge(pcs_df, left_on='NAME_1', right_on='state', how='left')
merged['pcs'] = merged['pcs'].fillna(0)

# 🛠️ Step 4: Get centroids for labeling
merged['centroid'] = merged.geometry.centroid
merged['lon'] = merged.centroid.x
merged['lat'] = merged.centroid.y

# ✅ Step 4.5: Create a separate GeoJSON for polygons only
choropleth_data = merged.drop(columns=['centroid', 'lon', 'lat'])


# Step 5: Create India-only map view
m = folium.Map(
    location=[22.9734, 78.6569],
    zoom_start=5,
    tiles='CartoDB positron'  # Clean background
)

# Step 6: Add shaded map
folium.Choropleth(
    geo_data=choropleth_data,  
    data=merged,
    columns=['NAME_1', 'pcs'],
    key_on='feature.properties.NAME_1',
    fill_color='YlGnBu',
    fill_opacity=0.8,
    line_opacity=0.3,
    legend_name='Number of Operational PCS',
).add_to(m)


# Step 7: Add labels directly on the map
for _, row in merged.iterrows():
    folium.map.Marker(
        [row['lat'], row['lon']],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color: rgba(255, 255, 255, 0.8);
                padding: 1px 30px;
                border-radius: 10px;
                box-shadow: 0px 0px 5px rgba(0,0,0,0.2);
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                color: #2c3e50;
                white-space: nowrap;
            ">
                {row['NAME_1'].title()}<br><span style="font-size:11px; font-weight:normal;">{int(row['pcs'])} PCS</span>
            </div>
            """
        )
    ).add_to(m)


# Step 8: Save and open map
m.save("pcs_map.html")
webbrowser.open('file://' + os.path.realpath("pcs_map.html"))
