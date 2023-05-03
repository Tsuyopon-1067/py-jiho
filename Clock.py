from datetime import datetime
import time
from TimeSchedule import TimeSchedule, ScheduleElement
from collections import deque
from SoundPlayer import Sound
from queue import Queue


class Clock:
    day: int = -1
    schedule = TimeSchedule().schedule
    dq: deque = deque()

    soundqueue: Queue[Sound] = Queue()

    def __init__(self, soundqueue: Queue[Sound]):
        self.soundqueue = soundqueue

    def run(self) -> None:
        while True:
            self.tick()
            wait: float = 1-float(datetime.now().strftime("0.%f"))
            time.sleep(wait)

    def tick(self) -> None:
        today_datetime_type = datetime.today()
        now: int = int(today_datetime_type.strftime("%H%M"))
        now_s: str = today_datetime_type.strftime("%H%:%M:%S")
        print(now_s)

        today: int = int(today_datetime_type.strftime("%d"))
        if (self.day != today):
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

        print(nextstr)

        return

    def _nextstr(self, s: str, v: ScheduleElement) -> str:
        time: str = "{:02d}:{:02d}".format(int(v.time/100), v.time % 100)
        return s + ": " + v.name + "(" + time + "): " + v.sound
