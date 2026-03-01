# src/audio_engine.py
import os
import random
import threading
from playsound import playsound

from src.config import REACTION_VOLUME


def get_clips(directory):
    # Returns all mp3 files in the given directory as full paths
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".mp3")
    ]


def play_random_clip(directory):
    clips = get_clips(directory)
    if not clips:
        return

    clip = random.choice(clips)
    thread = threading.Thread(target=playsound, args=(clip,), daemon=True)
    thread.start()


def init_audio():
    pass