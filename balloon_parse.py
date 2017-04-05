# balloon_parse.py
# Intakes, parses, and
# plots GPS and Sensor data

<<<<<<< HEAD
# -*- coding: utf-8 -*-

import codecs
import matplotlib as plt

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
    return lat

def get_lon(line):
    lon = mk_float(line[4])
    return lon

def get_alt(line):
    alt = mk_float(line[9])
    return alt

myfile = codecs.open('gpsdata.txt', 'r',encoding='utf-8', errors='ignore')

data = myfile.read().split('\n')

gpgga = []

for line in data:
    if line.startswith("$GPGGA") and line is not None:

        gpgga.append(line.strip().split(','))

# Necessary GPS Data
hours = []
minutes = []
seconds = []
lat = []
lon = []
alt = []

outfile = open('new_gpsdata.txt', 'w')
# Iterate through a copy of the data
for line in gpgga[:]:
    if len(line) >= 15:
        time = get_time(line)
        hours.append(time[0])
        minutes.append(time[1])
        seconds.append(time[2])

        lat.append(get_lat(line))
        lon.append(get_lon(line))
        alt.append(get_alt(line))
    else:
        gpgga.remove(line)

for i in range(len(hours)):
    print("Hours: %d Minutes: %d Seconds: %d" % (hours[i], minutes[i], seconds[i]))
    print("Latitude: %d Longitude: %d Altitude: %d" % (lat[i], lon[i], alt[i]))
=======
import codecs
from gps_parse import process_gps
import matplotlib as plt

myfile = codecs.open('gpsdata.txt', 'r', encoding='utf-8', errors='ignore')
data = myfile.read().split('\n')

gpgga = []
sensor_data = []

# Process GPGGA and sensor data
for line in data:
    data_list = line.strip().split(',')
    if data_list[0] == "$GPGGA" and data_list[] and len(data_list) == 15:
        gpgga.append(process_gps(data_list))
    elif data_list[0] == "SENSORS" and len(data_list) == 10:
        sensor_data.append(data_list)
    else:
        data.remove(line)

# TODO: implement sensor_parse.py

# TODO: 

# TODO: Sync time in GPGGA and Sensor_data

# TODO: merge GPGGA and Sensor_data into "balloon_data" according to time

# TODO: Organize balloon_data into a pandas dataframe

# TODO: Plot data

for i in range(len(hours)):
    print("Hours: {0} Minutes: {1} Seconds: {2}\n".format(hours[i], minutes[i], seconds[i])
    print("Latitude: {3} Longitude: {4} Altitude: {5}".format(lat[i], -lon[i], alt[i]))


# FOR GOOGLE MAPS COORDINATES
# print("new google.maps.LatLng(%f,-%f)," % (lat[i], lon[i]))
>>>>>>> restructure-gps-parse
