# SENSOR,HUMIDITY,TEMP,TEMP2,PRESSURE,ACC_X,ACC_Y,ACC_Z,BATTERY_VOLTAGE,TIME

# LAT,LON,ALT,TIME

import codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as scp

import gps_parse as gp
import sensor_parse as sp

flightfile = codecs.open('FlightData.txt', 'r', encoding='utf-8', errors='ignore')
funcfile = codecs.open('sensors.txt', 'r', encoding='utf-8', errors='ignore')

flightdata = flightfile.read().replace('\r', '').split('\n')
funcdata = funcfile.read().split('\r')
funcdata = [line.split(',') for line in funcdata][:30894]

gps_header = ['Seconds', 'Latitude', 'Longitude', 'Altitude']
sensor_header = ['Humidity', 'Internal Temperature', 'External Temperature',
                 'Pressure', 'Acceleration X', 'Acceleration Y',
                 'Acceleration Z', 'Battery Voltage', 'Seconds']

gps_parsed = []
sensor_parsed = []

# Get first valid minutes
for line in flightdata:
    line = line.strip().split(',')
    if(gp.check_gps(line)):
        gps_time_start = gp.get_seconds(line)
        break

debug = open('debug.txt', 'w+')

for line in flightdata:
    line = line.strip().split(',')
    if gp.check_gps(line):
        gps_row = [gp.get_seconds(line) - gps_time_start, gp.get_lat(line),
                   gp.get_lon(line), gp.get_alt(line)]
        gps_parsed.append(gps_row)
    elif sp.check_sensor(line):
        line = [float(x) for x in line[1:]]
        if(len(sensor_parsed) >= 18688):
            line[-1] += 6487564
        line[-1] = line[-1] / 1000
        sensor_parsed.append(line)

# Convert sensor and gps data into pandas dataframes and
# merge by 'Seconds'
df = pd.merge(pd.DataFrame(gps_parsed, columns=gps_header),
              pd.DataFrame(sensor_parsed, columns=sensor_header),
              how="outer", on='Seconds')

# Extract functional voltage from functional test data
funcdf = pd.DataFrame(funcdata, columns=sensor_header, dtype='float')
funcdf.rename(columns={"Battery Voltage":"Functional Voltage"}, inplace=True)
funcdf['Seconds'] /= 1000

pd.merge(df, funcdf[['Seconds', 'Functional Voltage']],
         on='Seconds', how='left')

df['Minutes'] = df['Seconds'] / 60

# Humidity
hum_i = 33  # percent
hum_v_i = 1.72  # initial voltage
hum_f = 100  # percent
hum_v_f = 5.06  # final voltage

# Calibration curves
hum_range = np.arange(0.0, 100, 0.1)  # percent
hum_slope = (hum_v_f - hum_v_i) / (hum_f - hum_i)
hum_int = hum_v_i - (hum_slope * hum_i)

df['Humidity'] = (df['Humidity'] - hum_int) / hum_slope
for i in range(50):
    df['Humidity'] = scp.savgol_filter(df['Humidity'], 19, 2)

plt.figure(1)
plt.subplot(211)
plt.plot(hum_range, (hum_slope * hum_range) + hum_int, lw=2)
plt.ylim(0.0, 5.0)
plt.xlabel('Humidity (# )', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)
plt.title('Humidity Calibration Curve', fontsize=14)

plt.subplot(212)
df.plot(x='Minutes', y='Humidity', ax=plt.gca())
plt.title('Humidity Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Humidity (# )', fontsize=10)

# Internal Temperature
temp_i = 22.2
temp_v_i = 3.17
temp_f = 4.0
temp_v_f = 2.83

temp_range = np.arange(-55, 150, 1)
temp_slope = (temp_v_f - temp_v_i) / (temp_f - temp_i)
temp_int = temp_v_i - (temp_slope * temp_i)

df['Internal Temperature'] = (df['Internal Temperature'] - temp_int) / temp_slope

for i in range(50):
    df['Internal Temperature'] = scp.savgol_filter(df['Internal Temperature'], 19, 2)

threshold = .25
for i in range(1, len(df)):
    if abs(df['Internal Temperature'][i] - df['Internal Temperature'][i - 1]) > threshold:
        df['Internal Temperature'][i] = df['Internal Temperature'][i - 1]

plt.figure(2)
plt.subplot(211)
plt.plot(temp_range, temp_slope * temp_range + temp_int, lw=2)
plt.ylim(0.0, 5.0)
plt.title('Internal Temperature Calibration Curve', fontsize=14)
plt.xlabel('Temperature (°C)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)

plt.subplot(212)
df.plot(x='Minutes', y='Internal Temperature', ax=plt.gca())
plt.title('Internal Temperature Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Temperature (°C)', fontsize=10)

# External Temperature
temp_outside_i = 22.2  # (Degrees C)
temp_outside_v_i = 3.14
temp_outside_f = -40.  # Not real
temp_outside_v_f = 2.35

# slope and y intercept
temp_outside_range = np.arange(-55, 150, 0.1)
temp_outside_slope = ((temp_outside_v_f - temp_outside_v_i) /
                      (temp_outside_f - temp_outside_i))
temp_outside_int = temp_outside_v_i - (temp_outside_slope * temp_outside_i)

df['External Temperature'] = (df['External Temperature'] - temp_outside_int) / temp_outside_slope
for i in range(50):
    df['External Temperature'] = scp.savgol_filter(df['External Temperature'], 19, 2)

plt.figure(3)
plt.subplot(211)
plt.plot(temp_outside_range, temp_outside_slope *
         temp_outside_range + temp_outside_int, lw=2)
plt.ylim(0.0, 5.0)
plt.title('External Temperature Calibration Curve', fontsize=14)
plt.xlabel('Temperature (°C)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)

plt.subplot(212)
df.plot(x='Minutes', y='External Temperature', ax=plt.gca())
plt.title('External Temperature Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Temperature (°C)', fontsize=10)

# PRESSURE
pres_i = 0.0
pres_v_i = 0.0
pres_f = 29.62
pres_v_f = 3.97
# slope and y intercept
pres_slope = (pres_v_f - pres_v_i) / (pres_f - pres_i)
pres_int = pres_v_i - (pres_slope * pres_i)


pres_range = np.arange(0, 40, 0.1)
plt.figure(4)
plt.subplot(211)
plt.plot(pres_range, (pres_slope * pres_range) + pres_int, lw=2)
plt.ylim(0.0, 5.0)
plt.title('Pressure Calibration Curve', fontsize=14)
plt.xlabel('Pressure (inMg)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)

df['Pressure'] = (df['Pressure'] - pres_int / pres_slope)

for i in range(10):
    df['Pressure'] = scp.savgol_filter(df['Pressure'], 19, 2)

plt.subplot(212)
plt.plot(df['Minutes'], df['Pressure'], lw=2)
plt.title('Pressure Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Pressure (inMg)', fontsize=10)

# Acceleration x
ax_i = -1
ax_v_i = 1.52
ax_f = 1
ax_v_f = 1.81
# slope and y intercept
ax_slope = (ax_v_f - ax_v_i) / (ax_f - ax_i)
ax_int = ax_v_i - (ax_slope * ax_i)

df['Acceleration X'] = (df['Acceleration X'] - ax_int) / ax_slope

for i in range(10):
    df['Acceleration X'] = scp.savgol_filter(df['Acceleration X'], 19, 2)

# Acceleration Y
ay_i = -1
ay_v_i = 1.63
ay_f = 1
ay_v_f = 1.83
# slope and y intercept
ay_slope = (ay_v_f - ay_v_i) / (ay_f - ay_i)
ay_int = ay_v_i - (ay_slope * ay_i)

df['Acceleration Y'] = (df['Acceleration Y'] - ay_int) / ay_slope

for i in range(10):
    df['Acceleration Y'] = scp.savgol_filter(df['Acceleration Y'], 19, 2)


# Acceleration Z
az_i = -1
az_v_i = 1.58
az_f = 1
az_v_f = 1.78
# slope and y intercept
az_slope = (az_v_f - az_v_i) / (az_f - az_i)
az_int = az_v_i - (az_slope * az_i)

df['Acceleration Z'] = (df['Acceleration Z'] - az_int) / az_slope

for i in range(10):
    df['Acceleration Z'] = scp.savgol_filter(df['Acceleration Z'], 19, 2)

acceleration_range = np.arange(-10, 10, 0.1)

plt.figure(5)
plt.subplot(211)
plt.plot(acceleration_range, (ax_slope * acceleration_range) + ax_int, lw=2)
plt.plot(acceleration_range, (ay_slope * acceleration_range) + ay_int, lw=2)
plt.plot(acceleration_range, (az_slope * acceleration_range) + az_int, lw=2)

plt.title('Acceleration Calibration Curve', fontsize=14)
plt.xlabel('Acceleration (g)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)
plt.legend(('X', 'Y', 'Z'), loc='upper right')

plt.subplot(212)
plt.plot(df['Minutes'], df['Acceleration X'], lw=2)
plt.plot(df['Minutes'], df['Acceleration Y'], lw=2)
plt.plot(df['Minutes'], df['Acceleration Z'], lw=2)
plt.title('Acceleration Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Acceleration (g)', fontsize=10)
plt.legend(('X', 'Y', 'Z'), loc='lower left')

# Battery

df['Battery Voltage'] *= 2
for i in range(10):
    df['Battery Voltage'] = scp.savgol_filter(df['Battery Voltage'], 19, 2)

plt.figure(6)
plt.plot(df['Minutes'], df['Internal Temperature'], lw=2)
plt.plot(df['Minutes'], df['Battery Voltage'], lw=2)
plt.plot(df['Minutes'], df['Functional Voltage'], lw=2)


plt.title('Analysis of Battery Voltage Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)

plt.ylabel('Temperature (°C)', fontsize=10)
plt.ylim(-20, 20)

plt.ylim(0, 8.5)
plt.ylabel('Voltage (V)', fontsize=10)

plt.legend('Balloon Launch Voltage',
           'Functional Test Voltage',
           'Balloon Launch Internal Temperature',
           loc='lower right')

plt.show()


"""
# Printing to google maps html format
google_maps = open("google_maps.txt", "w+")
for list in gpgga:
    if list[4] > 83 and list[4] < 85:
        google_maps.write("new google.maps.LatLng({},-{}),".format(list[3], list[4]))
        google_maps.write("\n")
"""
