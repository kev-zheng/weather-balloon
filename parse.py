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
>>>>>>> restructure-gps-parse
