"""
Author: David Teuscher
Last Edited: 30.03.22
This script takes books by Dostoevsky and songs by Viktor Tsoy
and does topic modeling for each group. Then the weights for
each topic over time are calculated and the trends over time
are shown
"""

# Import modules
import pandas as pd
import os
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string
import pymystem3
from gensim import corpora
import gensim
from pyLDAvis import gensim_models
from pyLDAvis import save_html

# Change directory to folder with text files for Doestoevsky's works
os.chdir("Dostoevsky/")



# Define a function to take a text file and turn it into a string
def file2str(pathway):
    with open(pathway, encoding="utf8") as infile:
        return infile.read().replace("\n", " ").replace(u'\xa0', u' ')

# Initialize a stemmer for Russian words
mystem = pymystem3.Mystem()
# Extract Russian stopwords and add additional ones to the list as well
russian_stopwords = stopwords.words("russian") + ["твой", "наш", "это", "--", "\"", "–", "—",
                                                  "…", ",", "...", "…", "»", "«", "-"]


# Preprocess function for the text
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in string.punctuation]

    text = " ".join(tokens).replace(",", " ").replace("«", " ").replace("–", " ").replace("--", " ").replace("—", " ").replace("-", " ").replace("»", " ").replace("\"", " ").replace("::", " ")

    return text

# Clean up novels
# Get the filenames for all the files
# filenames = [i for i in os.listdir() if re.search(r"\.txt", i)]

# # Make the text of all the files a string
# doc_complete = [file2str(i) for i in filenames]
#
# Clean up the text from the books
# books_complete = [preprocess_text(i) for i in doc_complete]
# Split the books up into words
# books_complete = [book.split() for book in books_complete]
#
# Create a corpora from the books
# corpus = corpora.Dictionary(books_complete)
#
# Create the document term matrix
# doc_term_matrix = [corpus.doc2bow(book) for book in books_complete]
#
# Move back to the original directory
# os.chdir("../")
# Initialize the LDA model
# Lda = gensim.models.ldamodel.LdaModel
# # Fit with 4 topics
# lda_model = Lda(doc_term_matrix, num_topics=4, id2word=corpus, passes=50)
# # Visualize the topics and save as HTML file
# visualization = gensim_models.prepare(lda_model, doc_term_matrix, corpus)
# save_html(visualization, "visualization_books.html")

# Read in file of songs
songs = pd.read_csv("songs.txt", sep="\t")
# Combine all lyrics together
song_lyrics = []
for song in songs[' Lyrics']:
    lyrics = song.replace("\n", " ").replace("...", " ")
    song_lyrics.append(lyrics)

# Clean up the text for the lyrics
songs_complete = [preprocess_text(i) for i in song_lyrics]
# Split the lyrics for each song into words
songs_complete = [song.split() for song in songs_complete]
# Create a corpora from the song lyrics
corpus = corpora.Dictionary(songs_complete)

# Create the document term matrix for the songs
doc_term_matrix = [corpus.doc2bow(song) for song in songs_complete]

# Initialize the LDA model
Lda = gensim.models.ldamodel.LdaModel
# Fit with 4 topics
lda_model = Lda(doc_term_matrix, num_topics=4, id2word=corpus, passes=50)
# Visualize the topics and save as HTML file
visualization = gensim_models.prepare(lda_model, doc_term_matrix, corpus)
save_html(visualization, "visualization_songs.html")

# Create an empty data frame to contain the topic and the weight of the topic for each
# document
weights_output = pd.DataFrame(columns = ['topic', 'prob_weight', 'doc_id'])

# Loop through each document and pull off the weights for each topic
for i in range(0, len(doc_term_matrix)):
    # Get the weights for each document
    doc_weights = lda_model[doc_term_matrix[i]]
    # Add the weights into the data frame
    weights_df = pd.DataFrame(doc_weights, columns = ['topic', 'prob_weight'])
    # Add the document number
    weights_df['doc_id'] = i
    # Append the data frame for the ith document to the previous documents processed
    weights_output = weights_output.append(weights_df)

# Save the topics weights by document to a .csv file
weights_output.to_csv("topic_weights_bydoc.csv")