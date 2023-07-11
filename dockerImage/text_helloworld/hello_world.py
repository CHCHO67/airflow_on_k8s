import pytz
from datetime import datetime
import time


def write_hello_world():
    seoul_tz = pytz.timezone("Asia/Seoul")
    now = datetime.now(seoul_tz)
    with open("/data/hello_world.txt", "w") as f:
        f.write(f"Hello World, Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    write_hello_world()
    time.sleep(120)
