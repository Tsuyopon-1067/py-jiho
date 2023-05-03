from playsound import playsound
from queue import Queue

import time


class Sound:
    name: str
    sleep: float

    def __init__(self, name: str, sleep: float):
        self.name = name
        self.sleep = sleep


class SoundPlayer:
    soundqueue: Queue[Sound] = Queue()

    def __init__(self, soundqueue: Queue[Sound]):
        self.soundqueue = soundqueue

    def run(self):
        while True:
            if self.soundqueue.empty():
                time.sleep(1)
                continue

            sound: Sound = self.soundqueue.get()
            playsound(sound.name)
            time.sleep(sound.sleep)
