import json
from typing import Dict

class ScheduleElement:
    name: str
    time: int
    sound: str
    def __init__(self, data: Dict[str, str]) -> None :
        self.name = data["name"]
        self.time = int(data["time"])
        self.sound = data["sound"]

    def print(self) -> None:
        print(self.name + ": " + str(self.time) + ", " + self.sound)

    def str(self) -> str:
        return "[" + self.name + ": " + str(self.time) + ", " + self.sound + "]"



class TimeSchedule:
    schedule: list[ScheduleElement] = []

    def __init__(self) -> None:
        file = open("chime.json", "r")
        data = json.load(file)["ChimeSettings"]
        for v in data:
            self.schedule.append(ScheduleElement(v))
        self.schedule = sorted(self.schedule, key=_gettime_for_sort)

    def print(self) -> None:
        for v in self.schedule:
            print(v)

    def str(self) -> str:
        res: str = ""
        res += "[\n"
        for v in self.schedule:
            res += v.str()
            res += "\n"
        res += "]"
        return res

def _gettime_for_sort(x: ScheduleElement) -> int:
    return -x.time