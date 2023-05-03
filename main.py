from datetime import datetime
import time
from TimeSchedule import TimeSchedule

def main() -> None:
	ts = TimeSchedule()
	clock()

def clock() -> None:
	while True:
		tick()
		time.sleep(1)

def tick() -> None:
	today_datetime_type = datetime.today()
	now = int(today_datetime_type.strftime("%H%M"))
	now_s = today_datetime_type.strftime("%H%:%M:%S")
	print(now_s)

if __name__ == "__main__":
    main()

