from datetime import datetime
import time
from TimeSchedule import TimeSchedule, ScheduleElement
from playsound import playsound
from collections import deque


def main() -> None:
    clock()


def clock() -> None:
    day: int = -1
    schedule = TimeSchedule().schedule
    dq: deque = deque()
    while True:
        day = tick(day, schedule, dq)
        time.sleep(1)


def tick(day: int, schedule: list[ScheduleElement], dq: deque) -> int:
    today_datetime_type = datetime.today()
    now: int = int(today_datetime_type.strftime("%H%M"))
    now_s: str = today_datetime_type.strftime("%H%:%M:%S")
    print(now_s)

    today: int = int(today_datetime_type.strftime("%d"))
    if (day != today):
        day = today
        for v in schedule:
            dq.append(v)

    nextstr: str = ""

    top: ScheduleElement
    if len(dq) == 0:
        nextstr = "next day"
    else:
        top = dq.pop()

        if top.time <= now:
            playsound(top.sound)
            if len(dq) == 0:
                nextstr = "next day"
            else:
                next: ScheduleElement = dq.pop()
                dq.append(next)
                nextstr = _nextstr("playing", next)
        else:
            dq.append(top)
            nextstr = _nextstr("next", top)

    print(nextstr)

    return day


def _nextstr(s: str, v: ScheduleElement) -> str:
    time: str = "{:02d}:{:02d}".format(int(v.time/100), v.time % 100)
    return s + ": " + v.name + "(" + time + "): " + v.sound


if __name__ == "__main__":
    main()
