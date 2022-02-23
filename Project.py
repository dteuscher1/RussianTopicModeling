from bs4 import BeautifulSoup as bs
import requests
import justext
import urllib.parse

url = "https://lyric-text.ru/viktor-tsoy/"

# Specify header information related to your computer
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
# Make a request to the web page
response = requests.get(url, headers=headers)
# Parse the HTML content on the page
soup = bs(response.content, "html.parser")
paragraphs = soup.find_all("div", {'class': 'content_box'})
links = []
for paragraph in paragraphs:
    anchors = paragraph.find_all('a')
    for anchor in anchors:
        try:
            links.append(anchor.attrs['href'])
        except KeyError:
            print("skipping this anchor because it doesn't have an href attribute")



def get_absolute_path_link(url, relative_link):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.urljoin(parsed_url.scheme + "://" + parsed_url.netloc, relative_link)

# Get the absolute path for each link
links = [get_absolute_path_link(url, l) for l in links]

print(links)
# current_url = links[0]
# try:
#     response = requests.get(current_url, headers=headers)
# except:
#     print("Nothing")
# paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
# for paragraph in paragraphs:
#     print(paragraph.text)


