import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")

# --- LOAD DATA ---
# Ensure 'imdb_top_1000.csv' is in the same directory
try:
    df = pd.read_csv('imdb_top_1000.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'imdb_top_1000.csv' not found. Please upload the file.")

# --- DATA CLEANING (Task 1 & General) ---
[cite_start]# [cite: 13] Remove commas from 'Gross' and convert to numeric
if df['Gross'].dtype == 'O': # Check if object/string type
    df['Gross'] = df['Gross'].str.replace(',', '', regex=False)
df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')

# Drop rows with missing Gross revenue as they can't be analyzed for financial success
df_clean = df.dropna(subset=['Gross']).copy()

# ==========================================
# TASK 1: DIRECTOR ANALYSIS
# ==========================================

[cite_start]# [cite: 15] Filter: Directors with at least 3 movies
director_counts = df_clean['Director'].value_counts()
reliable_directors = director_counts[director_counts >= 3].index
df_directors = df_clean[df_clean['Director'].isin(reliable_directors)]

[cite_start]# [cite: 14] Calculate Total Gross Revenue per Director
director_revenue = df_directors.groupby('Director')['Gross'].sum().sort_values(ascending=False)

# Select Top 10 for the chart
top_10_directors = director_revenue.head(10)

[cite_start]# [cite: 16] Visualization: Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_directors.values, y=top_10_directors.index, palette='viridis')
plt.title('Top 10 Directors by Total Gross Revenue (Min. 3 Movies)', fontsize=16, weight='bold')
plt.xlabel('Total Gross Revenue', fontsize=12)
plt.ylabel('Director', fontsize=12)
plt.tight_layout()

[cite_start]# [cite: 40] Save plot
plt.savefig('director_revenue.png')
plt.show()

# ==========================================
# TASK 2: GENRE ANALYSIS
# ==========================================

[cite_start]# [cite: 21] Data Transformation: Explode the Genre column
df_clean['Genre_List'] = df_clean['Genre'].str.split(', ')
df_exploded = df_clean.explode('Genre_List')

[cite_start]# [cite: 22-27] Aggregation: Avg Rating, Avg Gross, and Count per Genre
genre_stats = df_exploded.groupby('Genre_List').agg({
    'IMDB_Rating': 'mean',
    'Gross': 'mean',
    'Series_Title': 'count'
}).rename(columns={'Series_Title': 'Movie_Count'})

[cite_start]# [cite: 28] Filtering: Remove genres with < 10 movies
genre_stats = genre_stats[genre_stats['Movie_Count'] >= 10]

[cite_start]# [cite: 29-35] Visualization: Scatter Plot (Bubble Chart)
plt.figure(figsize=(14, 8))
sns.scatterplot(
    data=genre_stats,
    x='IMDB_Rating',
    y='Gross',
    size='Movie_Count',
    sizes=(100, 1000),
    hue=genre_stats.index,
    alpha=0.7,
    legend=False
)

# Label the bubbles
for genre in genre_stats.index:
    plt.text(
        genre_stats.loc[genre, 'IMDB_Rating'] + 0.02,
        genre_stats.loc[genre, 'Gross'],
        genre,
        fontsize=9,
        weight='bold'
    )

plt.title('Genre Performance: Critical Acclaim vs. Commercial Success', fontsize=16, weight='bold')
plt.xlabel('Average IMDB Rating', fontsize=12)
plt.ylabel('Average Gross Revenue', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

[cite_start]# [cite: 40] Save plot
plt.savefig('genre_analysis.png')
plt.show()

print("\nAnalysis Complete. Images saved as 'director_revenue.png' and 'genre_analysis.png'.")