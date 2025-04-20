
# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(forcats)
library(stringr)
library(readr)

# Load the cleaned data
netflix_data <- read_csv("netflix_cleaned.csv")


# Display basic information about the dataset
cat("Dataset structure:\n")
str(netflix_data)

cat("\nSummary statistics:\n")
summary(netflix_data)

# Data preparation for genre analysis
# Function to split the genres
extract_genres <- function(genre_string) {
  if (is.na(genre_string)) {
    return(NA)
  }
  
  genres <- strsplit(genre_string, ",")[[1]]
  genres <- trimws(genres)
  return(genres)
}

# Apply function to each row and create a long format data frame
all_genres <- netflix_data %>%
  filter(!is.na(listed_in)) %>%
  rowwise() %>%
  mutate(genre_list = list(extract_genres(listed_in))) %>%
  unnest(genre_list)

# Count genres
genre_counts <- all_genres %>%
  count(genre_list, sort = TRUE) %>%
  rename(genre = genre_list, count = n)

# Visualization 1: Top 15 Genres (similar to Python version)
top_genres <- genre_counts %>%
  slice_max(count, n = 15)

# Create the plot
p1 <- ggplot(top_genres, aes(x = reorder(genre, count), y = count)) +
  geom_bar(stat = "identity", fill = "#2C3E50") +
  coord_flip() +
  theme_minimal() +
  labs(
    title = "Top 15 Netflix Genres",
    x = "Genre",
    y = "Count",
    caption = "Source: Netflix Dataset"
  ) +
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    axis.title = element_text(size = 12),
    axis.text = element_text(size = 10)
  )

# Save the plot
ggsave("top_genres_r.png", p1, width = 12, height = 8, dpi = 300)
# Display the plot
print(p1)

# Visualization 2: Content Type by Rating
rating_type_data <- netflix_data %>%
  filter(!is.na(rating)) %>%
  group_by(rating, type) %>%
  summarise(count = n(), .groups = "drop") %>%
  arrange(desc(count))

# Create the plot
p2 <- ggplot(rating_type_data, aes(x = reorder(rating, -count), y = count, fill = type)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  scale_fill_manual(values = c("Movie" = "#E74C3C", "TV Show" = "#3498DB")) +
  labs(
    title = "Content Distribution by Rating and Type",
    x = "Rating",
    y = "Count",
    fill = "Content Type",
    caption = "Source: Netflix Dataset"
  ) +
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    axis.title = element_text(size = 12),
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    legend.position = "top"
  )

# Save the plot
ggsave("rating_by_type_r.png", p2, width = 12, height = 8, dpi = 300)
# Display the plot
print(p2)

cat("\nR analysis completed successfully!\n")
cat("Visualizations saved as PNG files.\n")
