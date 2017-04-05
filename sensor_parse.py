# SENSOR,HUMIDITY,TEMP,TEMP2,PRESSURE,ACC_X,ACC_Y,ACC_Z,BATTERY_VOLTAGE,TIME


def mk_float(s):
    s = s.strip()
    return float(s) if s else 0


def get_humidity(line):
    humidity = mk_float(line[1])
    return humidity


def get_temp_one(line):
    temp = mk_float(line[2])
    return temp


def get_temp_two(line):
    temp = mk_float(line[3])
    return temp


def get_pressure(line):
    pressure = mk_float(line[4])
    return pressure


def get_ax(line):
    ax = mk_float(line[5])
    return ax


def get_ay(line):
    ay = mk_float(line[6])
    return ay


def get_az(line):
    az = mk_float(line[7])
    return az


def get_battery(line):
    return False

def get_sensor_time(line):
    return False


def check_sensor(line):
    list = line.strip().split(',')
    if list[0] == "SENSORS" and len(list) == 10:
        return True
    return False
