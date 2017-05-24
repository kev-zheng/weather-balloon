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
google_maps = open('google_maps.txt', 'w+')
kml = open('kml.txt', 'w+')
kml.write("Latitude, Longitude, Altitude")

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

for line in flightdata:
    line = line.strip().split(',')
    if gp.check_gps(line):
        seconds = gp.get_seconds(line) - gps_time_start
        lat = gp.get_lat(line)
        lon = gp.get_lon(line)
        alt = gp.get_alt(line)
        if(alt > 10):
            gps_row = [seconds, lat, lon, alt]
            gps_parsed.append(gps_row)
            # Printing to google maps
            google_maps.write("new google.maps.LatLng({}, -{}),".format(lat, lon))
            google_maps.write("\n")
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
df['Minutes'] = df['Seconds'] / 60

# Calibration curve calculations

# Humidity
hum_i = 33  # percent
hum_v_i = 1.72  # initial voltage
hum_f = 100  # percent
hum_v_f = 5.06  # final voltage
hum_slope = (hum_v_f - hum_v_i) / (hum_f - hum_i)
hum_int = hum_v_i - (hum_slope * hum_i)
hum_range = np.arange(0.0, 100, 0.1)

# Internal Temperature
temp_i = 22.2  # Degrees C
temp_v_i = 3.17
temp_f = 4
temp_v_f = 2.83
temp_slope = (temp_v_f - temp_v_i) / (temp_f - temp_i)
temp_int = temp_v_i - (temp_slope * temp_i)

# External Temperature
temp_outside_i = 22.2  # Degrees C
temp_outside_v_i = 3.14
temp_outside_f = -40.
temp_outside_v_f = 2.35
temp_outside_range = np.arange(-55, 150, 0.1)
temp_outside_slope = ((temp_outside_v_f - temp_outside_v_i) /
                      (temp_outside_f - temp_outside_i))
temp_outside_int = temp_outside_v_i - (temp_outside_slope * temp_outside_i)

temp_range = np.arange(-55, 150, 1)

# PRESSURE
pres_i = 0.0
pres_v_i = 0.0
pres_f = 29.62
pres_v_f = 3.97
pres_slope = (pres_v_f - pres_v_i) / (pres_f - pres_i)
pres_int = pres_v_i - (pres_slope * pres_i)
pres_range = np.arange(0, 40, 0.1)

# Acceleration x
ax_i = -1
ax_v_i = 1.52
ax_f = 1
ax_v_f = 1.81
ax_slope = (ax_v_f - ax_v_i) / (ax_f - ax_i)
ax_int = ax_v_i - (ax_slope * ax_i)

# Acceleration Y
ay_i = -1
ay_v_i = 1.63
ay_f = 1
ay_v_f = 1.83
ay_slope = (ay_v_f - ay_v_i) / (ay_f - ay_i)
ay_int = ay_v_i - (ay_slope * ay_i)

# Acceleration Z
az_i = -1
az_v_i = 1.58
az_f = 1
az_v_f = 1.78
az_slope = (az_v_f - az_v_i) / (az_f - az_i)
az_int = az_v_i - (az_slope * az_i)
acceleration_range = np.arange(-10, 10, 0.1)

# Conversion from voltage to real values 
df['Humidity'] = (df['Humidity'] - hum_int) / hum_slope
df['Internal Temperature'] = (df['Internal Temperature'] - temp_int) / temp_slope
df['External Temperature'] = (df['External Temperature'] - temp_outside_int) / temp_outside_slope
df['Pressure'] = (df['Pressure'] - pres_int) / pres_slope
df['Acceleration X'] = (df['Acceleration X'] - ax_int) / ax_slope
df['Acceleration Y'] = (df['Acceleration Y'] - ay_int) / ay_slope
df['Acceleration Z'] = (df['Acceleration Z'] - az_int) / az_slope
df['Battery Voltage'] *= 2

# Extract functional voltage from functional test data
funcdf = pd.DataFrame(funcdata, columns=sensor_header, dtype='float')
funcdf.rename(columns={"Battery Voltage":"Functional Voltage"}, inplace=True)
funcdf['Functional Voltage'] *= 2
funcdf['Seconds'] = round(funcdf['Seconds'] / 1000)
funcdf['Minutes'] = funcdf['Seconds'] / 60

# Savitz-golay filter
for i in range(10):
    df['Humidity'] = scp.savgol_filter(df['Humidity'], 19, 2)
    df['Internal Temperature'] = scp.savgol_filter(df['Internal Temperature'], 19, 2)
    df['External Temperature'] = scp.savgol_filter(df['External Temperature'], 19, 2)
    df['Pressure'] = scp.savgol_filter(df['Pressure'], 19, 2)
    df['Acceleration X'] = scp.savgol_filter(df['Acceleration X'], 19, 2)
    df['Acceleration Y'] = scp.savgol_filter(df['Acceleration Y'], 19, 2)
    df['Acceleration Z'] = scp.savgol_filter(df['Acceleration Z'], 19, 2)
    df['Battery Voltage'] = scp.savgol_filter(df['Battery Voltage'], 19, 2)

# Smooth outliers in temperature data
internal_temp = df['Internal Temperature']
thresh = .25
for i in range(1, len(internal_temp)):
    if abs(internal_temp.iloc[i] - internal_temp.iloc[i - 1]) > thresh:
        internal_temp.iloc[i] = internal_temp.iloc[i - 1]

df['Internal Temperature'] = internal_temp
""" PLOTTING """
# Calibration Curves
plt.figure(1)
#plt.suptitle("Sensor Calibration Curves", fontsize=14)
ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=2)
ax5 = plt.subplot2grid((2, 6), (1, 3), colspan=2)

ax1.plot(hum_range, (hum_slope * hum_range) + hum_int, lw=2)
ax1.set_ylim(0.0, 5.0)
ax1.set_xlabel('Humidity (%)', fontsize=10)
ax1.set_ylabel('Voltage (V)', fontsize=10)
ax1.set_title('Humidity', fontsize=14)

ax2.plot(temp_range, temp_slope * temp_range + temp_int, lw=2)
ax2.set_ylim(0.0, 5.0)
ax2.set_title('Internal Temperature', fontsize=14)
ax2.set_xlabel('Temperature (°C)', fontsize=10)
ax2.set_ylabel('Voltage (V)', fontsize=10)

ax3.plot(temp_outside_range, temp_outside_slope *
         temp_outside_range + temp_outside_int, lw=2)
ax3.set_ylim(0.0, 5.0)
ax3.set_title('External Temperature', fontsize=14)
ax3.set_xlabel('Temperature (°C)', fontsize=10)
ax3.set_ylabel('Voltage (V)', fontsize=10)

ax4.plot(acceleration_range, (ax_slope * acceleration_range) + ax_int, lw=2)
ax4.plot(acceleration_range, (ay_slope * acceleration_range) + ay_int, lw=2)
ax4.plot(acceleration_range, (az_slope * acceleration_range) + az_int, lw=2)
ax4.set_title('Acceleration', fontsize=14)
ax4.set_xlabel('Acceleration (g)', fontsize=10)
ax4.set_ylabel('Voltage (V)', fontsize=10)
ax4.legend(('X', 'Y', 'Z'), loc='upper left')

ax5.plot(pres_range, (pres_slope * pres_range) + pres_int, lw=2)
ax5.set_ylim(0.0, 5.0)
ax5.set_title('Pressure', fontsize=14)
ax5.set_xlabel('Pressure (inHg)', fontsize=10)
ax5.set_ylabel('Voltage (V)', fontsize=10)

plt.tight_layout()

plt.figure(2)
df.plot(x='Minutes', y='Humidity', ax=plt.gca())
#plt.title('Humidity Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Humidity (%)', fontsize=10)

plt.figure(3)
df.plot(x='Minutes', y='Internal Temperature', ax=plt.gca())
#plt.title('Internal and External Temperature Over Time', fontsize=14)
df.plot(x='Minutes', y='External Temperature', ax=plt.gca())
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Temperature (°C)', fontsize=10)

plt.figure(5)
plt.plot(df['Minutes'], df['Pressure'], lw=2)
#plt.title('Pressure Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Pressure (inHg)', fontsize=10)

plt.figure(6)
plt.plot(df['Minutes'], df['Acceleration X'], lw=2)
plt.plot(df['Minutes'], df['Acceleration Y'], '#FFCC00', lw=2)
plt.plot(df['Minutes'], df['Acceleration Z'], '#FF6600', lw=2)
#plt.title('Acceleration Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Acceleration (g)', fontsize=10)
plt.legend(('X', 'Y', 'Z'), loc='lower left')

plt.figure(7)
plt.plot(df['Minutes'], df['Altitude'], lw=2)
#plt.title('Altitude Over Time', fontsize=14)
plt.xlabel('Time (min)', fontsize=10)
plt.ylabel('Altitude (M)', fontsize=10)

fig, ax1 = plt.subplots()
#ax1.set_title('Analysis of Battery Voltage and Temperature Over Time', fontsize=14)
temp_line = ax1.plot(df['Minutes'], df['Internal Temperature'], lw=2, color='#FF6600')
ax1.set_xlabel('Time (min)', fontsize=10)
ax1.set_ylabel('Internal Temperature (°C)', color='#FF6600')
ax1.set_ylim([-20, 20])

ax2 = ax1.twinx()
volt_line = ax2.plot(df['Minutes'], df['Battery Voltage'], lw=2, color='b')
func_line = ax2.plot(funcdf['Minutes'], funcdf['Functional Voltage'], color='b', ls='--')
ax2.set_ylabel('Voltage (V)', fontsize=10, color='b')
ax2.set_ylim([0, 8.5])

lns = temp_line + volt_line + func_line
lbs = [l.get_label() for l in lns]
ax1.legend(lns, lbs, loc='lower left')

fig, ax1 = plt.subplots()
#ax1.set_title('Analysis of Temperature and Altitude over Time', fontsize=14)
alt_line = ax1.plot(df['Minutes'], df['Altitude'], lw=2)
ax1.set_xlabel('Time (min)', fontsize=10)
ax1.set_ylabel('Altitude (m)')

ax2 = ax1.twinx()
temp_line = ax2.plot(df['Minutes'], df['External Temperature'], lw=2, color='#FF6600')
ax2.set_ylabel('External Temperature (°C)', fontsize=10, color='#FF6600')
plt.legend([alt_line, temp_line], ['Altitude', 'External Temperature'])

lns = alt_line + temp_line
lbs = [l.get_label() for l in lns]
ax1.legend(lns, lbs, loc=0)

plt.show()
