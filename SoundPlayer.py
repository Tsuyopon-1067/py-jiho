from playsound import playsound
from queue import Queue

import time


class Sound:
    # 鳴らす音声の情報
    name: str  # 音声ファイル名
    sleep: float  # 音声を鳴らしてからのsleep秒数

    def __init__(self, name: str, sleep: float):
        self.name = name
        self.sleep = sleep


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
            playsound(sound.name)  # 音声を鳴らして指定秒数待つ
            time.sleep(sound.sleep)
