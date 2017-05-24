# SENSOR,HUMIDITY,TEMP,TEMP2,PRESSURE,ACC_X,ACC_Y,ACC_Z,BATTERY_VOLTAGE,TIME

def check_sensor(list):
    if list[0] == "SENSORS" and len(list) == 10:
        return True
    return False
