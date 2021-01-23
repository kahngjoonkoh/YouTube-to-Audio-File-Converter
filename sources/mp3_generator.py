from sources.browser import *
from pytube import YouTube
from moviepy.editor import *
import os
import shutil
import eyed3


def get_mp3(url, file_name, artist, title, album=None):
    try:
        print(f"Converting {file_name}")

        print(f"Fetching YouTube video")
        mp4 = YouTube(url).streams.get_highest_resolution().download()
        new_file_name = ""
        for char in file_name:
            if char in "`\/?<>*&^%#}{[]":
                char = ""
            new_file_name += char

        mp3 = f"{new_file_name}.mp3"

        print(f"Starting mp3 format conversion")
        video_clip = VideoFileClip(mp4)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3, codec="libmp3lame")

        audio_clip.close()
        video_clip.close()


        os.remove(mp4)
        print(f"Editing mp3 metadata")
        track = eyed3.load(mp3)

        track.tag.artist = artist
        track.tag.title = title
        track.tag.album = album
        track.tag.albumartist = artist
        print("Getting lyrics data")
        lyrics = get_lyrics(artist, title)
        if lyrics is not False:
            track.tag.lyrics.set(lyrics)
            print("Lyrics set")
            track.tag.save()
        elif lyrics is False:
            print("No lyrics data")
        print(f"{url} conversion complete")
        try:
            shutil.move(mp3, r"output")
        except shutil.Error:
            print("File already exists")
            os.remove(mp3)
        else:
            print("moved into output file")
        return True
    except shutil.Error:
        return False
