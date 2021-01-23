import urllib.request
import requests
import bs4
import re
from langdetect import detect

allowed_characters = "abcdefghijklmnopqrstuvwxyz_.\-~"


def get_yt_link(keywords):
    query = keywords.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}+audio"
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return f"https://www.youtube.com/watch?v={video_ids[0]}"

# TODO:
def get_yt_title(link):
    link = "Link"
    return link


def get_lyrics(artist, title):
    lang = detect(f"{artist} {title}")
    if lang is "ko":
        return get_lyrics_ko(artist, title)
    else:
        return get_lyrics_eng(artist, title)


def get_lyrics_eng(artist, title):
    new_artist = ""
    new_title = ""
    for char in artist.lower():
        if char not in allowed_characters:
            char = ""
        new_artist += char
    if "(feat." in title:
        start = title.index("(feat.")
        title = title[:start-1]
    for char in title.lower():
        if char not in allowed_characters:
            char = ""
        new_title += char

    url = f"http://www.azlyrics.com/lyrics/{new_artist}/{new_title}.html"
    url = url.lower()
    # Getting Source and extracting lyrics
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        raw_lyrics = soup.find_all("div", class_=False, id=False)
        lyrics = raw_lyrics[0].get_text()
        return lyrics
    except ValueError:
        return False
    except urllib.error.HTTPError:
        return False


def get_lyrics_ko(artist, title):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    url = f"https://www.melon.com/search/lyric/index.htm?q={urllib.parse.quote(artist)}+{urllib.parse.quote(title)}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form".replace(" ", "+")
    # Getting Source and extracting lyrics
    req = requests.get(url, headers=header)
    html = req.text.encode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    raw_lyric_page = str(soup.find("dd", class_="lyric").a)
    proc_lyric_page = raw_lyric_page.split(";")[1]
    lyric_num_index = proc_lyric_page.index("'")
    song_id = proc_lyric_page[lyric_num_index+1:-2]

    lyric_url = f"https://www.melon.com/song/detail.htm?songId={song_id}"
    print(lyric_url)

    req2 = requests.get(lyric_url, headers=header)
    html2 = req.text.encode('utf-8')
    soup2 = bs4.BeautifulSoup(html2, 'html.parser')
    text = soup2.get_text
    index = text.index("lyric")
    #lyric_section = soup2.find_all("dd", class_="lyric")
    #lyrics = lyric_section[0]

    #lyrics = raw_lyrics[0].get_text()
    return index

# print(get_lyrics_ko("SEVENTEEN", "울고 싶지 않아"))
