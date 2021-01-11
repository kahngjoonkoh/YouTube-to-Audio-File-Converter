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
        print(soup)
        key = "<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing " \
              "agreement. Sorry about that. --> "
        where_start = re.findall(key, text)
        print(text)
        print(where_start)
        start = where_start[0] + 26
        where_end = html.find('<!-- end of lyrics -->')
        end = where_end - 2
        lyrics = html[start:end].replace('<br />', '').decode("UTF8")
        print(lyrics)
        return lyrics
    except urllib.error.HTTPError:
        print("Can't find lyrics")