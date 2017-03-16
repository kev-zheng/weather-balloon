# gps_parse.py
# GPS Helper functions for balloon_parse.py


def mk_float(s):
    s = s.strip()
    return float(s) if s else 0

#  get_time returns an array in the format
#  of [ hours, minutes, seconds ]
def get_time(line):
    time = round(float(line[1]))
    seconds = time % 100
    time //= 100
    minutes = time % 100
    time //= 100
    hours = time % 100
    return [hours, minutes, seconds]


def get_lat(line):
    lat = mk_float(line[2])
    degrees = lat // 100
    minutes = (lat % 100) / 60
    return degrees + minutes


def get_lon(line):
    lon = mk_float(line[4])
    degrees = lon // 100
    minutes = (lon % 100) / 60
    return degrees + minutes


def get_alt(line):
    alt = mk_float(line[9])
    return alt


def process_gps(line):
    gps = get_time(line)
    gps += [get_alt(line), get_lon(line), get_alt(line)]
