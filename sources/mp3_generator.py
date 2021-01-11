import browser
from pytube import YouTube
from moviepy.editor import *
import os
import shutil
import eyed3


def get_mp3(url, file_name, artist, title, album=None):
    print(f"Converting {file_name}")

    print(f"Fetching YouTube video")
    mp4 = YouTube(url).streams.get_highest_resolution().download()
    mp3 = f"{file_name}.mp3"

    print(f"Starting mp3 format conversion")
    video_clip = VideoFileClip(mp4)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3)

    audio_clip.close()
    video_clip.close()


    os.remove(mp4)
    print(f"Editing mp3 metadata")
    track = eyed3.load(mp3)

    track.tag.artist = artist
    track.tag.title = title
    track.tag.album = album
    track.tag.albumartist = artist
    track.tag.lyrics.set(browser.get_lyrics(artist, title))
    print(track.tag.lyrics)
    track.tag.save()

    print(f"{url} conversion complete")
    shutil.move(mp3, r"output")