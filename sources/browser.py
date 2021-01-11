import urllib.request
import bs4
import re

allowed_characters = "abcdefghijklmnopqrstuvwxyz_.\-~"


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
    new_artist = ""
    new_title = ""
    for char in artist.lower():
        if char not in allowed_characters:
            char = ""
        new_artist += char

    for char in title.lower():
        if char not in allowed_characters:
            char = ""
        new_title += char

    url = f"http://www.azlyrics.com/lyrics/{new_artist}/{new_title}.html"
    url = url.lower()
    # Getting Source and extracting lyrics
    try:
        print(1)
        html = urllib.request.urlopen(url).read().decode('utf-8')
        print(2)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        print(3)
        raw_lyrics = soup.find_all("div", class_=False, id=False)
        print(4)
        lyrics = raw_lyrics[0].get_text()
        print(5)
        return lyrics
    except:
        print(6)
        return False

