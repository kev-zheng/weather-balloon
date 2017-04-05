# balloon_parse.py
# Intakes, parses, and
# plots GPS and Sensor data

# SENSOR,HUMIDITY,TEMP,TEMP2,PRESSURE,ACC_X,ACC_Y,ACC_Z,BATTERY_VOLTAGE,TIME

# LAT,LON,ALT,TIME

import codecs

import gps_parse as gp
import sensor_parse as sp

myfile = codecs.open('FlightData.txt', 'r', encoding='utf-8', errors='ignore')

data = myfile.read().replace('\r', '\n').split('\n')

gpgga = []
sensor_data = []

gps = open("gps.txt", "w+")
sensors = open("sensors.txt", "w+")
gps_formatted = open("gpgga.txt", "w+")

gps_formatted.write("Hours,Minutes,Seconds,Lat,Lon,Alt\n")

for line in data:
    line = line.strip()
    if gp.check_gps(line):
        gps.write(line)
        gps.write("\n")
        line = line.split(',')
        list = gp.get_gps_time(line)
        list.append(gp.get_lat(line))
        list.append(gp.get_lon(line))
        list.append(gp.get_alt(line))

        gpgga.append(list)
        gps_formatted.write(','.join(map(str, list)))
        gps_formatted.write('\n')

    elif sp.check_sensor(line):
        sensor_data.append(line.split(','))
        if(len(sensor_data) >= 18688):
            sensors.write(line[8:-2] + ',' + str(int(line[-1]) + 6487564))
        else:
            sensors.write(line[8:])
        sensors.write('\n')

google_maps = open("google_maps.txt", "w+")

for list in gpgga:
    if list[4] > 83 and list[4] < 85:
        google_maps.write("new google.maps.LatLng({},-{}),".format(list[3], list[4]))
        google_maps.write("\n")
