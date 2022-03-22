from bs4 import BeautifulSoup as bs
import requests
import justext
import urllib.parse

urls = ["https://lyric-text.ru/viktor-tsoy/", "https://lyric-text.ru/viktor-tsoy/page-2/",
        "https://lyric-text.ru/viktor-tsoy/page-3/", "https://lyric-text.ru/viktor-tsoy/page-4/"]

links = []
song_title = []
for url in urls:
    # Specify header information related to your computer
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    # Make a request to the web page
    response = requests.get(url, headers=headers)
    # Parse the HTML content on the page
    soup = bs(response.content, "html.parser")
    paragraphs = soup.find_all("div", {'class': 'content_box'})
    for paragraph in paragraphs:
        anchors = paragraph.find_all('a')
        for anchor in anchors:
            try:
                links.append(anchor.attrs['href'])
                song_title.append(anchor.get_text())
            except KeyError:
                print("skipping this anchor because it doesn't have an href attribute")



def get_absolute_path_link(url, relative_link):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.urljoin(parsed_url.scheme + "://" + parsed_url.netloc, relative_link)

# Get the absolute path for each link
links = [get_absolute_path_link(url, l) for l in links]

print(links)
print(song_title)
current_url = links[0]

with open(f"songs.txt", mode='w') as outfile:
    outfile.write("Title" + "\t" + " Lyrics" + '\n')
    for i in range(len(links)):
        response = requests.get(links[i], headers=headers)
        # Parse the HTML content on the page
        soup = bs(response.content, "html.parser")
        paragraphs = soup.find('div', {'class': 'content_box'}).find('p')
        try:
            outfile.write(song_title[i] + "\t" + paragraphs.get_text(strip=True) + '\n')
            print(f'Writing {song_title[i]}')
        except:
            print("No text. Moving to next link")
            continue



