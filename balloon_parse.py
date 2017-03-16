# balloon_parse.py
# Intakes, parses, and
# plots GPS and Sensor data

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
    if data_list[0] == "$GPGGA" and len(data_list) == 15:
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
