import pandas as pd
import os
import re

songs = pd.read_csv("songs.txt", sep="\t")
os.chdir("Dostoevsky/")


# Clean up novels
# Get the filenames for all the files

def file2str(pathway):
    with open(pathway, encoding="utf8") as infile:
        return infile.read().replace("\n", " ").replace(u'\xa0', u' ')

filenames = [i for i in os.listdir() if re.search(r"\.txt", i)]
# Make the text of all the files a string
doc_complete = [file2str(i) for i in filenames]

# Combine all lyrics together
song_lyrics = []
for song in songs[' Lyrics']:
    lyrics = song.replace("\n", " ").replace("...", " ")
    song_lyrics.append(lyrics)
print(song_lyrics)
