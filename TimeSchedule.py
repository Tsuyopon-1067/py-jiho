import json
from typing import Dict


class ScheduleElement:
    # チャイムを鳴らすべき時間1つについての情報を保存
    # printとstrメソッドは基本デバック用
    name: str  # 科目名とか
    time: int  # 鳴らす時間
    sound: str  # 鳴らしたい音声ファイルの場所

    def __init__(self, data: Dict[str, str]) -> None:
        self.name = data["name"]
        self.time = int(data["time"])
        self.sound = data["sound"]

    def print(self) -> None:
        print(self.name + ": " + str(self.time) + ", " + self.sound)

    def str(self) -> str:
        return "[" + self.name + ": " + str(self.time) + ", " + self.sound + "]"


class TimeSchedule:
    # チャイムを鳴らすべき時間（スケジュール）についての情報を保存
    # printとstrメソッドは基本デバック用
    schedule: list[ScheduleElement] = []  # 一通り入れる配列

    def __init__(self) -> None:
        file = open("chime.json", "r")
        data = json.load(file)["ChimeSettings"]  # Jsonの情報を取得
        # Json中で1スケジュールをScheduleElement型に変換して配列に入れる
        for v in data:
            self.schedule.append(ScheduleElement(v))
        # 時間で早い順にソートする
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
