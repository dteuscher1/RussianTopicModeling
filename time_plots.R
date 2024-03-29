# Load package
library(tidyverse)

# Read in song weights
song_weights <- read.csv("songs_weights.csv")
# Plot the topic weights for songs over time
ggplot(song_weights, aes(x = Year, y = average_weight, color = topic_label)) +
    geom_smooth(se = FALSE) + 
    labs(y = "Average Topic Weight", color = "Topic", 
         title = "Topics over Time for Songs by Viktor Tsoi") +
    theme_minimal() +
    theme(legend.position = "bottom")

# Read in the book weights
book_weights <- read.csv("books_weights.csv")
# Plot the topic weights for books over time
ggplot(book_weights, aes(x = Year, y = average_weight, color = topic_label)) +
    geom_smooth(se = FALSE) + 
    labs(y = "Average Topic Weight", color = "Topic", 
         title = "Topics over Time for Works by Dostoevsky") +
    theme_minimal() +
    theme(legend.position = "bottom")
