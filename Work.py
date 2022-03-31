"""
Author: David Teuscher
Last Edited: 30.03.22
This script takes news articles and performs topic modeling for the articles.
The top 10 words for the topics are written out to a .csv file.
"""

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

songs = pd.read_csv("songs.txt", sep="\t")
os.chdir("Dostoevsky/")


# Clean up novels
# Get the filenames for all the files

def file2str(pathway):
    with open(pathway, encoding="utf8") as infile:
        return infile.read().replace("\n", " ").replace(u'\xa0', u' ')

mystem = pymystem3.Mystem()
russian_stopwords = stopwords.words("russian") + ["твой", "наш", "это", "--", "\"", "–", "—",
                                                  "…", ",", "...", "…", "»", "«", "-"]


# Preprocess function
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in string.punctuation]

    text = " ".join(tokens).replace(",", " ").replace("«", " ").replace("–", " ").replace("--", " ").replace("—", " ").replace("-", " ").replace("»", " ").replace("\"", " ").replace("::", " ")

    return text
#
# filenames = [i for i in os.listdir() if re.search(r"\.txt", i)]
# # Make the text of all the files a string
# doc_complete = [file2str(i) for i in filenames]
#
# books_complete = [preprocess_text(i) for i in doc_complete]
# books_complete = [book.split() for book in books_complete]
# corpus = corpora.Dictionary(books_complete)
#
# doc_term_matrix = [corpus.doc2bow(book) for book in books_complete]
#
# os.chdir("../")
# Lda = gensim.models.ldamodel.LdaModel
# # Fit with 4 topics
# lda_model = Lda(doc_term_matrix, num_topics=4, id2word=corpus, passes=50)
# # Visualize the topics and save as HTML file
# visualization = gensim_models.prepare(lda_model, doc_term_matrix, corpus)
# save_html(visualization, "visualization_books.html")
# Combine all lyrics together
song_lyrics = []
for song in songs[' Lyrics']:
    lyrics = song.replace("\n", " ").replace("...", " ")
    song_lyrics.append(lyrics)


songs_complete = [preprocess_text(i) for i in song_lyrics]
songs_complete = [song.split() for song in songs_complete]
corpus = corpora.Dictionary(songs_complete)

doc_term_matrix = [corpus.doc2bow(song) for song in songs_complete]

Lda = gensim.models.ldamodel.LdaModel
# Fit with 4 topics
lda_model = Lda(doc_term_matrix, num_topics=4, id2word=corpus, passes=50)
# Visualize the topics and save as HTML file
visualization = gensim_models.prepare(lda_model, doc_term_matrix, corpus)
save_html(visualization, "visualization_songs.html")

# Extract the top words for each topic
#setup data-frame
weights_output = pd.DataFrame(columns = ['topic', 'prob_weight', 'doc_id'])

#extraction loop
for i in range(0, len(doc_term_matrix)):
    doc_weights = lda_model[doc_term_matrix[i]]
    weights_df = pd.DataFrame(doc_weights, columns = ['topic', 'prob_weight'])
    weights_df['doc_id'] = i
    weights_output = weights_output.append(weights_df)

#save information in the format you use
weights_output.to_csv("topic_weights_bydoc.csv")