from datetime import datetime
import time
from TimeSchedule import TimeSchedule, ScheduleElement
from collections import deque
from SoundPlayer import Sound
from queue import Queue
import light_sensor


class Clock:
    # 時計を動かすクラス
    # チャイムを鳴らすべき時間になるとsoundqueueに音声情報を入れる　その後SoundPlayerクラスがいろいろやってくれる
    day: int = -1  # 今日の日付が入る 日付が変わってチャイムをリセットするときに使う
    schedule = TimeSchedule().schedule  # チャイムを鳴らすべき時間情報の配列
    dq: deque = deque()  # チャイムキュー 普通のキューよりちょっと早いらしいからdequeを使う チャイムを鳴らしたい時間が早い順に入れておく
    _title: str = ""  # 2つともテキスト時計表示用
    _underline: str = ""

    # スレッド間通信用キュー 鳴らしたい音声の情報を入れてSoundPlayerクラスに再生してもらう
    soundqueue: Queue[Sound] = Queue()

    def __init__(self, soundqueue: Queue[Sound]):
        self.soundqueue = soundqueue  # mainからスレッド間通信用キューをもらう
        self._createtitle()  # 時計タイトル表示用テキストをつくるだけ

    def run(self) -> None:
        while True:
            self.tick()  # 毎秒実行
            # 現在？.xx秒 -> 1-0.xx秒待てば秒が変わるときに更新できる
            wait: float = 1-float(datetime.now().strftime("0.%f"))
            time.sleep(wait)

    def tick(self) -> None:
        # 毎秒実行する
        today_datetime_type = datetime.today()
        now: int = int(today_datetime_type.strftime("%H%M"))  # チャイム鳴らすタイミング判定用
        now_s: str = today_datetime_type.strftime("%H:%M:%S")  # 時計表示用

        today: int = int(today_datetime_type.strftime("%d"))  # 今日の日付
        if self.day != today:  # 日付が変わったらチャイムキューをリセットして補充し直す
            self.day = today
            self.dq.clear()
            for v in self.schedule:
                self.dq.append(v)

        # nextstr: 次になるチャイムの情報
        # nextstrをもらいつつ必要であればチャイムを鳴らす
        nextstr: str = self.trychime(now)
        self._printtitle(now_s, nextstr)
        # print(now_s, nextstr)
        return

    def trychime(self, now: int) -> str:
        # 鳴らすべきならチャイムを鳴らす
        top: ScheduleElement
        if len(self.dq) == 0:
            # キューが空っぽなら明日鳴らす
            return self._nextstr("next day", self.schedule[len(self.schedule)-1])

        top = self.dq.pop()  # 一回今から最も早い時間チャイムの情報をもらう まだだったら後で戻す

        if top.time <= now:  # 鳴らすべき時刻を過ぎてるので鳴らしたい
            if light_sensor.is_open() and top.time == now:  # 部屋が明るければ鳴らす
                sound: Sound = Sound(top.sound, top.category, top.value)
                self.soundqueue.put(sound)  # 別スレッドに情報を渡す

            if len(self.dq) == 0:  # チャイムをならしてキューがからっぽなら次に鳴らすのは明日
                return self._nextstr("next day", self.schedule[len(self.schedule)-1])
            else:  # まだ次に鳴らすチャイムがあるならそれを表示する
                next: ScheduleElement = self.dq.pop()  # さらにキューから一つ取って戻す
                self.dq.append(next)
                return self._nextstr("playing", next)
        else:  # まだ鳴らすべき時間でないときはtopがnextの情報なのでキューに戻して表示する
            self.dq.append(top)
            return self._nextstr("next", top)

    def _nextstr(self, s: str, v: ScheduleElement) -> str:
        time: str = "{:02d}:{:02d}".format(int(v.time/100), v.time % 100)
        return s + ": " + v.name + "(" + time + "): " + v.sound

    def _printtitle(self, now_s: str, nextstr: str) -> None:
        # タイトル・時間・次チャイム情報を表示する
        # 毎秒見えるやつはこれ
        print("\033[2J")
        print(self._title)
        print("|")
        print("| \033[1m" + now_s + "\033[0m" + " -> " + nextstr)
        print(self._underline)

    def _createtitle(self) -> None:
        yoko: int = 30
        s: str = ""
        t: str = ""
        u: str = ""
        for i in range(0, yoko-1):
            s += "-"
        s += "/"

        t += "|"
        for i in range(0, int((yoko-17)/2)):
            t += " "
        t += "ITソルーション室"
        for i in range(0, int((yoko-17)/2)-1):
            t += " "
        t += "/"
        t += "    "
        t += "\033[3mでんちゃっちゃ時報\033[0m"

        for i in range(0, yoko-3):
            u += "-"
        u += "/"
        for i in range(0, 28):
            u += "-"

        self._title = s + "\n" + t + "\n" + u

        for i in range(0, 56):
            self._underline += "-"
