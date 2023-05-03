from datetime import datetime
import time
from TimeSchedule import TimeSchedule, ScheduleElement
from playsound import playsound


def main() -> None:
    clock()


def clock() -> None:
    before: int = -1  # 前に実行した時間
    schedule = TimeSchedule().schedule
    while True:
        before = tick(before, schedule)
        time.sleep(1)


def tick(before: int, schedule: list[ScheduleElement]) -> int:
    today_datetime_type = datetime.today()
    now: int = int(today_datetime_type.strftime("%H%M"))
    now_s: str = today_datetime_type.strftime("%H%:%M:%S")
    print(now_s)

    isend: bool = True
    nextstr: str = ""
    nextidx: int = 0
    for i in range(0, len(schedule)):
        if before < schedule[i].time:  # n側にまだ後のチャイムが登録されている
            isend = False
            nextidx = i
            if i+1 == len(schedule):
                continue
            if before < schedule[i+i].time and schedule[i+1].time < now:
                playsound(schedule[i+1].sound)
                before = now
                nextstr = _nextstr("playing", schedule, i+1)

    if nextstr == "":
        nextstr = _nextstr("next", schedule, nextidx)

    print(nextstr)

    if isend:
        before = -1

    return before


def _nextstr(s: str, schedule: list[ScheduleElement], i: int) -> str:
    v: ScheduleElement = schedule[i]
    time: str = str(int(v.time/100)) + ":" + str(v.time % 100)
    return s + ": " + v.name + "(" + time + "): " + v.sound


if __name__ == "__main__":
    main()
