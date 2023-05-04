from datetime import datetime
import time
from TimeSchedule import TimeSchedule, ScheduleElement
from collections import deque
from SoundPlayer import Sound
from queue import Queue
import light_sensor


class Clock:
    day: int = -1
    schedule = TimeSchedule().schedule
    dq: deque = deque()
    _title: str = ""
    _underline: str = ""

    soundqueue: Queue[Sound] = Queue()

    def __init__(self, soundqueue: Queue[Sound]):
        self.soundqueue = soundqueue
        self._createtitle()

    def run(self) -> None:
        while True:
            self.tick()
            wait: float = 1-float(datetime.now().strftime("0.%f"))
            time.sleep(wait)

    def tick(self) -> None:
        today_datetime_type = datetime.today()
        now: int = int(today_datetime_type.strftime("%H%M"))
        now_s: str = today_datetime_type.strftime("%H%:%M:%S")

        today: int = int(today_datetime_type.strftime("%d"))
        if self.day != today:
            self.day = today
            for v in self.schedule:
                self.dq.append(v)

        nextstr: str = ""

        top: ScheduleElement
        if len(self.dq) == 0:
            nextstr = "next day"
        else:
            top = self.dq.pop()

            if top.time <= now:
                if light_sensor.is_open():
                    sound: Sound = Sound(top.sound, 0.1)
                    self.soundqueue.put(sound)

                if len(self.dq) == 0:
                    nextstr = "next day"
                else:
                    next: ScheduleElement = self.dq.pop()
                    self.dq.append(next)
                    nextstr = self._nextstr("playing", next)
            else:
                self.dq.append(top)
                nextstr = self._nextstr("next", top)

        self._printtitle(now_s, nextstr)
        # print(now_s, nextstr)
        return

    def _nextstr(self, s: str, v: ScheduleElement) -> str:
        time: str = "{:02d}:{:02d}".format(int(v.time/100), v.time % 100)
        return s + ": " + v.name + "(" + time + "): " + v.sound

    def _printtitle(self, now_s: str, nextstr: str) -> None:
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
