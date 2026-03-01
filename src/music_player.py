# src/music_player.py
# Plays background music on a loop in a separate thread.
# Non-blocking — main loop never waits for it.

import threading
import time
from playsound import playsound

from src.config import MUSIC_PATH


def _music_loop():
    while True:
        playsound(MUSIC_PATH)    # playsound blocks until clip finishes, then loops


def start_music_thread():
    thread = threading.Thread(target=_music_loop, daemon=True)
    thread.start()