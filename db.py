import sqlite3
import pandas as pd

# Connect to SQLite DB
conn = sqlite3.connect('ev_india.db')

# Load and insert CSV into SQLite
df_EV_Maker_by_Place = pd.read_csv('csv/EV Maker by Place.csv')
df_EV_Maker_by_Place.to_sql('EV_Maker_by_Place', conn, if_exists='replace', index=False)

df_ev_category = pd.read_csv('csv/ev_category.csv')
df_ev_category.to_sql('ev_category', conn, if_exists='replace', index=False)

df_ev_sales_by_makers_and_cat = pd.read_csv('csv/ev_sales_by_makers_and_cat.csv')
df_ev_sales_by_makers_and_cat.to_sql('ev_sales_by_makers_and_cat', conn, if_exists='replace', index=False)

df_OperationalPC = pd.read_csv('csv/OperationalPC.csv')
df_OperationalPC.to_sql('OperationalPC', conn, if_exists='replace', index=False)

df_Vehicle_Class = pd.read_csv('csv/Vehicle Class.csv')
df_Vehicle_Class.to_sql('Vehicle_Class', conn, if_exists='replace', index=False)

# cursor = conn.cursor()
# cursor.execute("SELECT * from EV_Maker_by_Place;")
# tables = cursor.fetchall()
# for row in tables:
#     print(row[0])