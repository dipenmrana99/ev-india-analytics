import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Connect to DB
conn = sqlite3.connect('ev_india.db')
df = pd.read_sql_query("SELECT * FROM ev_sales_by_makers_and_cat", conn)
conn.close()

# Identify year columns
year_columns = [col for col in df.columns if col.isnumeric()]
df[year_columns] = df[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Total sales across all years
df['Total'] = df[year_columns].sum(axis=1)

# Unique categories
categories = df['Category'].unique()
num_categories = len(categories)

# Setup grid layout (e.g. 2 rows, 3 cols for 6 categories)
cols = 2
rows = math.ceil(num_categories / cols)

# Figure size adapts to number of categories
fig, axes = plt.subplots(rows, cols, figsize=(14, 5 * rows))
axes = axes.flatten()

# Plot per category
for i, category in enumerate(categories):
    ax = axes[i]
    cat_df = df[df['Category'] == category].sort_values(by='Total', ascending=False).head(5)
    sns.barplot(x='Total', y='Maker', data=cat_df, ax=ax, palette='Set2')
    ax.set_title(f"Top 5 EV Makers - {category}", fontsize=12)
    # ax.set_xlabel("Total Sales (2015–2024)", fontsize=11)
    # ax.set_ylabel("Maker", fontsize=11)
    ax.tick_params(axis='y', labelsize=10)

# Hide empty subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Overall layout
plt.suptitle("Top 5 EV Makers by Category (2015-2024)", fontsize=16)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.show()
