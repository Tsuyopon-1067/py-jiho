from datetime import datetime
import time
from TimeSchedule import TimeSchedule, ScheduleElement
from playsound import playsound
from Clock import Clock


def main() -> None:
    clock = Clock()
    clock.clock()


if __name__ == "__main__":
    main()
