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
                                                  "…", ",", "...", "…", "»", "«", "-", "м", "когда", "э", "24", "то", "припев", "то", "весь", ":", "эй", "кто", "свой", "алеша", "свидригайлов", "митя", "старообрядец", "'", "иван", "федорович", "петрович", "ивановна", "наташа", "который", "!..", ")", "степан", "соня", "какой", "что", "нибудь", "ваш", "очень", ]


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
filenames = [i for i in os.listdir() if re.search(r"\.txt", i)]

# # Make the text of all the files a string
doc_complete = [file2str(i) for i in filenames]

# Clean up the text from the books
books_complete = [preprocess_text(i) for i in doc_complete]
# Split the books up into words
books_complete = [book.split() for book in books_complete]

# Create a corpora from the books
corpus = corpora.Dictionary(books_complete)

# Create the document term matrix
doc_term_matrix = [corpus.doc2bow(book) for book in books_complete]

# Move back to the original directory
os.chdir("../")
# Initialize the LDA model
Lda = gensim.models.ldamodel.LdaModel
# # Fit with 4 topics
lda_model = Lda(doc_term_matrix, num_topics=3, id2word=corpus, passes=50, random_state=360)
# # Visualize the topics and save as HTML file
visualization = gensim_models.prepare(lda_model, doc_term_matrix, corpus)
save_html(visualization, "visualization_books.html")

# Initialize a data frame to save the weights for each document and topic
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
weights_output.to_csv("topic_weights_bydoc_songs.csv")

# Load in the topic weights and the years for each book
df = pd.read_csv("topic_weights_bydoc_songs.csv")
df2 = pd.read_csv("Doestoevsky_Works_Years.csv")

# Reset the index and add the document number using the index
df3 = df2.reset_index()
df3['doc_id'] = df3.index

# Merge the weights and the years based on the document ID
df4 = pd.merge(df,df3[['doc_id','Year', 'Title']],on='doc_id', how='left')

# Determine the number of unique documents and name the columns
total_docs = df4.groupby('Year')['doc_id'].apply(lambda x: len(x.unique())).reset_index()
total_docs.columns = ['Year', 'total_docs']

# Add the weight based on year and topic
df_avg = df4.groupby(['Year', 'topic']).agg({'prob_weight':'sum'}).reset_index()

# Determine the average weight per topic per year
df_avg = df_avg.merge(total_docs, on='Year', how="left")
df_avg['average_weight'] = df_avg['prob_weight'] / df_avg['total_docs']

# Create a dataframe of topic labels
topic_labels = ["Люди (People)", "Психология людей (Psychology of humans)", "Действия (Actions)"]
topic_id = [0, 1, 2]
data_tuple = list(zip(topic_id, topic_labels))
df_labels = pd.DataFrame(data_tuple, columns = ['topic', 'topic_label'])

# Merge labels into year weights data and save to .csv file
df_avg2 = df_avg.merge(df_labels, on='topic')
df_avg2.to_csv("books_weights.csv")
