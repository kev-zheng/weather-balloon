import codecs

myfile = codecs.open('FlightData.txt', 'r', encoding='utf-8', errors='ignore')
data = myfile.read().replace('\r', '\n').split('\n')

data = list(filter(None, data))

gps_count = 0
sensor_count = 0

for line in data:
	print(line)
	if line.startswith("SENSOR"):
		sensor_count += 1
	elif line.strip() != '\n':
		gps_count += 1

print("Sensor lines: {}".format(sensor_count))
print("GPS lines: {}".format(gps_count))