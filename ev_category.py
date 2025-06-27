import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect('ev_india.db')
df = pd.read_sql_query("SELECT * FROM ev_category", conn)
conn.close()

# Convert 'Year' to int and calculate row-wise sum across all categories
df['Year'] = df['Year'].astype(int)

# Drop 'Year' column temporarily to sum other columns
category_columns = df.columns.drop('Year')
df['Total_EV'] = df[category_columns].sum(axis=1)

# Create a simple DataFrame with Year and Total
summary_df = df[['Year', 'Total_EV']].groupby('Year').sum().reset_index()

# Pivot into matrix format (Year as index and Total as value)
summary_matrix = summary_df.pivot_table(index='Year', values='Total_EV')

# Plot as heatmap
plt.figure(figsize=(8, 7))
sns.heatmap(summary_matrix, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={"label": "Total EVs"})
plt.title("Total EVs Sold Per Year (2001-2024)", fontsize=14)
plt.ylabel("Year")
plt.xlabel("")

plt.tight_layout()
plt.show()
