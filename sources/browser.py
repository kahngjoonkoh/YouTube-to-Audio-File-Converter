import urllib.request
import bs4
import re


def get_yt_link(keywords):
    query = keywords.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}+audio"
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return f"https://www.youtube.com/watch?v={video_ids[0]}"


def get_yt_title(link):
    link = "Link"
    return link


def get_lyrics(artist, title):
    url = f"http://www.azlyrics.com/lyrics/{artist}/{title}.html".replace(" ", "")
    url = url.lower()
    # Getting Source and extracting lyrics
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        raw_lyrics = soup.find_all("div", class_=False, id=False)
        lyrics = raw_lyrics[0].get_text()

        return lyrics
    except urllib.error.HTTPError:
        print("Can't find lyrics")