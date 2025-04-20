
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os

# Data Preparation
# Load the CSV file
netflix_df = pd.read_csv('Netflix_shows_movies.csv')

print("Data loaded successfully!")
print("\n------- Initial Data Overview -------")
print(f"Shape of the dataset: {netflix_df.shape}")
print("\nFirst 5 rows:")
print(netflix_df.head())

# Set the style for our visualizations
plt.style.use('fivethirtyeight')
sns.set_palette("deep")

# Data Cleaning
print("\n------- Missing Values Analysis -------")
missing_values = netflix_df.isnull().sum()
print(missing_values[missing_values > 0])

# Calculate percentage of missing values
percent_missing = (missing_values / len(netflix_df)) * 100
print("\nPercentage of missing values:")
print(percent_missing[percent_missing > 0])

# Handle missing values
# For categorical columns, fill with 'Unknown'
categorical_cols = ['director', 'cast', 'country', 'date_added']
for col in categorical_cols:
    if col in netflix_df.columns:
        netflix_df[col] = netflix_df[col].fillna('Unknown')

# For description, fill with a placeholder
if 'description' in netflix_df.columns:
    netflix_df['description'] = netflix_df['description'].fillna('No description available')

print("\nMissing values after cleaning:")
print(netflix_df.isnull().sum()[netflix_df.isnull().sum() > 0])

# Data Exploration
print("\n------- Data Exploration -------")
print("\nDataset Information:")
print(netflix_df.info())

print("\nDescriptive Statistics:")
print(netflix_df.describe())

print("\nContent type distribution:")
print(netflix_df['type'].value_counts())

print("\nRatings distribution:")
print(netflix_df['rating'].value_counts())

# Release year distribution
print("\nRelease year distribution:")
year_counts = netflix_df['release_year'].value_counts().sort_index()
print(year_counts)

# Data Preparation for Visualization
# Extract all genres from listed_in column
def extract_genres(genre_list):
    if isinstance(genre_list, str):
        return [genre.strip() for genre in genre_list.split(',')]
    return []

"""**Data Visualization**"""

def visualize_data(df):
    print("\n--- Data Visualization ---")

# Apply function to listed_in column
all_genres = []
for genres in netflix_df['listed_in']:
    all_genres.extend(extract_genres(genres))

# Count genre occurrences
genre_counts = Counter(all_genres)

# 1. Most watched genres visualization
plt.figure(figsize=(12, 8))
top_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:15])
sns.barplot(x=list(top_genres.values()), y=list(top_genres.keys()))
plt.title('Top 15 Netflix Genres', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Genre', fontsize=12)
plt.tight_layout()
plt.savefig('top_genres.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='type', data=netflix_df)
plt.title('Distribution of Content Types on Netflix', fontsize=16)
plt.xlabel('Content Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.tight_layout()
plt.savefig('content_type_distribution.png')
plt.show()  # Added plt.show() to display in notebook

# 3. Content type distribution (Movie vs TV Show)
plt.figure(figsize=(12, 8))
ratings_count = netflix_df['rating'].value_counts()
sns.barplot(x=ratings_count.index, y=ratings_count.values)
plt.title('Distribution of Content Ratings on Netflix', fontsize=16)
plt.xlabel('Rating', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ratings_distribution.png')
plt.show()

# 4. Temporal analysis: Content added over time
# Convert date_added to datetime
netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'], errors='coerce')
netflix_df['year_added'] = netflix_df['date_added'].dt.year
netflix_df['month_added'] = netflix_df['date_added'].dt.month

# Group by year and count
yearly_additions = netflix_df.groupby('year_added').size().reset_index(name='count')
yearly_additions = yearly_additions.dropna()

plt.figure(figsize=(12, 6))
sns.lineplot(x='year_added', y='count', data=yearly_additions, marker='o')
plt.title('Content Added to Netflix by Year', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Count of Titles Added', fontsize=12)
plt.xticks(yearly_additions['year_added'], rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('yearly_content_additions.png')
plt.show()  # Added plt.show() to display in notebook

# Extract numeric duration for movies
netflix_movies = netflix_df[netflix_df['type'] == 'Movie']

def extract_duration_min(duration_str):
    if isinstance(duration_str, str) and 'min' in duration_str:
        try:
            return int(re.search(r'(\d+) min', duration_str).group(1))
        except:
            return np.nan
    return np.nan

netflix_movies = netflix_df[netflix_df['type'] == 'Movie'].copy()  # Create an explicit copy
netflix_movies['duration_min'] = netflix_movies['duration'].apply(extract_duration_min)

plt.figure(figsize=(12, 6))
sns.histplot(netflix_movies['duration_min'].dropna(), bins=30, kde=True)
plt.title('Distribution of Movie Durations on Netflix', fontsize=16)
plt.xlabel('Duration (minutes)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('movie_duration_distribution.png')
plt.show()
plt.close()

print("\nData analysis and visualization completed successfully!")
print("Visualizations saved as PNG files.")

# Save the cleaned data for use in R
netflix_df.to_csv('netflix_cleaned.csv', index=False)
print("\nCleaned data saved to 'netflix_cleaned.csv' for R analysis.")

