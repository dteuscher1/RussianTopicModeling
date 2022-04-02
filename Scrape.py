"""
Author: David Teuscher
Last Edited: 30.03.22
This script takes scrapes the text for songs by Viktor Tsoy and
writes them to a .txt file
"""

# Load need packages
from bs4 import BeautifulSoup as bs
import requests
import justext
import urllib.parse

# URLs to scrape links from
urls = ["https://lyric-text.ru/viktor-tsoy/", "https://lyric-text.ru/viktor-tsoy/page-2/",
        "https://lyric-text.ru/viktor-tsoy/page-3/", "https://lyric-text.ru/viktor-tsoy/page-4/"]

# Create empty list for links and song title
links = []
song_title = []
# Loop through the four URLs to scrape from
for url in urls:
    # Specify header information related to your computer
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    # Make a request to the web page
    response = requests.get(url, headers=headers)
    # Parse the HTML content on the page
    soup = bs(response.content, "html.parser")
    # Find all the div tags with the specific class
    paragraphs = soup.find_all("div", {'class': 'content_box'})
    # Loop through each found div tag
    for paragraph in paragraphs:
        # Pull all the anchors out
        anchors = paragraph.find_all('a')
        # Try to take the href from the anchor tag if possible
        for anchor in anchors:
            try:
                links.append(anchor.attrs['href'])
                song_title.append(anchor.get_text())
            # print that the anchor is skipped if there is a KeyError resulting from no href attribute
            except KeyError:
                print("skipping this anchor because it doesn't have an href attribute")


# Create function to create the absolute path based on the relative link
def get_absolute_path_link(url, relative_link):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.urljoin(parsed_url.scheme + "://" + parsed_url.netloc, relative_link)

# Get the absolute path for each link
links = [get_absolute_path_link(url, l) for l in links]

# Open an output file for the songs
with open(f"songs.txt", mode='w') as outfile:
    # Write a header for the file
    outfile.write("Title" + "\t" + " Lyrics" + '\n')
    # Loop through the links
    for i in range(len(links)):
        # Get the HTML content
        response = requests.get(links[i], headers=headers)
        # Parse the HTML content on the page
        soup = bs(response.content, "html.parser")
        # Find all the divs with the specific class and then the paragraph inside
        paragraphs = soup.find('div', {'class': 'content_box'}).find('p')
        # Write out to text file if there is text
        try:
            outfile.write(song_title[i] + "\t" + paragraphs.get_text(strip=True) + '\n')
            print(f'Writing {song_title[i]}')
        except:
            print("No text. Moving to next link")
            continue



