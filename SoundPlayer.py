from playsound import playsound
from queue import Queue
import datetime

import time


class Sound:
    # 鳴らす音声の情報
    name: str  # 音声ファイル名
    category: str  # 種類
    value: str

    def __init__(self, name: str, category: str, value: str):
        self.name = name
        self.category = category
        self.value = value


class SoundPlayer:
    soundqueue: Queue[Sound] = Queue()  # 鳴らす音声を入れるキュー 別スレッドからキューに音声情報を入れてもらう

    def __init__(self, soundqueue: Queue[Sound]):
        self.soundqueue = soundqueue

    def run(self):
        while True:
            # 毎秒キューを監視する
            if self.soundqueue.empty():
                time.sleep(1)
                continue

            # キューが空じゃないとき以下を実行
            sound: Sound = self.soundqueue.get()  # キューから1つ音声をもらう
            if sound.category == "class_start":
                self.classstart(sound)
            elif sound.category == "class_end":
                self.classend(sound)
            elif sound.category == "before_close":
                self.beforeclose(sound)
            elif sound.category == "close":
                self.close(sound)
            elif sound.category == "time_signal":
                self.timesignal(sound)
            else:
                playsound(sound.name)

    def classstart(self, sound: Sound):
        weekday = datetime.date.today().weekday()
        if weekday > 4:
            return
        koma: str = "voice/c" + sound.value + ".mp3"
        playsound(sound.name)
        playsound("voice/c0.mp3")
        playsound(koma)
        playsound("voice/c98.mp3")

    def classend(self, sound: Sound):
        weekday = datetime.date.today().weekday()
        if weekday > 4:
            return
        koma: str = "voice/c" + sound.value + ".mp3"
        playsound(sound.name)
        time.sleep(0.3)
        playsound(koma)
        playsound("voice/c99.mp3")

    def beforeclose(self, sound: Sound):
        koma: str = "voice/e" + sound.value + ".mp3"
        playsound(sound.name)
        playsound("voice/e0.mp3")
        playsound(koma)
        playsound("voice/e99.mp3")

    def close(self, sound: Sound):
        playsound(sound.name)
        playsound("voice/end.mp3")
        
    def timesignal(self, sound: Sound):
        koma: str = "voice/j" + sound.value + ".mp3"
        playsound(sound.name)
        playsound(koma)
        playsound("voice/j99.mp3")
