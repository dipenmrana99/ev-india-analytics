import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from SQLite
conn = sqlite3.connect('ev_india.db')
df = pd.read_sql_query("SELECT * FROM Vehicle_Class", conn)
conn.close()

# Sort data
df_sorted = df.sort_values(by="Total Registration", ascending=False)

# Plot
plt.figure(figsize=(12, 7))
sns.barplot(x="Total Registration", y="Vehicle Class", data=df_sorted, palette="coolwarm")

# Get current Axes
ax = plt.gca()

# Loop through bars and add labels
for bar in ax.patches:
    width = bar.get_width()
    y_pos = bar.get_y() + bar.get_height() / 2
    label = f'{int(width):,}'
    
    ax.text(width + df_sorted["Total Registration"].max() * 0.01,  # Slightly to the right of the bar
            y_pos,
            label,
            va='center',
            fontsize=9)


plt.title("Total Vehicle Registrations by Vehicle Class in India", fontsize=12)
plt.xlabel("Total Registrations")
plt.ylabel("Vehicle Class")
plt.tight_layout()
plt.show()
