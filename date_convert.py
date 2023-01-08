from datetime import date
from time import mktime


def convert_to_unix(datetime: str) -> int:
    datetime = list(map(int, datetime.split(".")))
    datetime = date(*datetime[:3])

    unixtime = int(mktime(datetime.timetuple()))

    return unixtime
