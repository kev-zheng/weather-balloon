%%
clr;
v_range = [0 5];

data = csvread('flightsensor.txt', 0, 0);
funcdata = csvread('sensors.txt', 0, 0);

time = data(:, 9);
time(18689:end,:) = time(18689:end,:) + time(18688); %time data reset , this fixes that
time_sec = time ./ 1000;
time_min = time_sec ./ 60;

%% HUMIDITY

hum_v = data(:, 1)y;

%data points
hum_i = 33; %(percent)
hum_v_i = 1.72;
hum_f = 100; %(percent)
hum_v_f = 5.06;
%slope and y intercept
hum_slope = (hum_v_f - hum_v_i) / (hum_f - hum_i);
hum_int = hum_v_i - (hum_slope * hum_i);


hum_range = [0:100];
figure();
plot(hum_range, (hum_slope .* hum_range) + hum_int, 'LineWidth', 2);
axis ([hum_range(1) hum_range(end) v_range]);
title('Humidity Calibration Curve','fontsize',14);
xlabel('Humidity (%)','fontsize',10);
ylabel('Voltage (V)','fontsize',10);


cal_hum = (hum_v - hum_int) ./ hum_slope;
cal_hum_filt = cal_hum;

for x = 1 : 10;
    cal_hum_filt = sgolayfilt(cal_hum_filt, 2, 19);
end

figure();
plot(time_min, cal_hum_filt, 'LineWidth', 2);
title('Humidity Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);
ylabel('Humidity (%)','fontsize',10);
%% TEMPERATURE

temp_v = data(:, 2);

%data points
temp_i = 22.2; %(Degrees C)
temp_v_i = 3.17;
temp_f = 4; 
temp_v_f = 2.83;
%slope and y intercept
temp_slope = (temp_v_f - temp_v_i) / (temp_f - temp_i);
temp_int = temp_v_i - (temp_slope * temp_i);

temp_range = [-55:150];
figure();
plot(temp_range, (temp_slope .* temp_range) + temp_int, 'LineWidth', 2);
axis ([temp_range(1) temp_range(end) v_range]);
title('Internal Temperature Calibration Curve','fontsize',14);
xlabel('Temperature (^\circ C)','fontsize',10);
ylabel('Voltage (V)','fontsize',10);


cal_temp = (temp_v - temp_int) ./ temp_slope;
cal_temp_filt = cal_temp;

for x = 1 : 10;
    cal_temp_filt = sgolayfilt(cal_temp_filt, 2, 19);
end

thresh = .25;
cal_temp_filt(1) = 5;
for x = 1:length(cal_temp_filt)-1
    d = diff (cal_temp_filt);
    if d(x) > thresh | d(x) < -thresh
        cal_temp_filt(x+1) = cal_temp_filt(x);
    end
end

for x = 1 : 10;
    cal_temp_filt = sgolayfilt(cal_temp_filt, 2, 19);
end

figure();
plot(time_min, cal_temp_filt, 'LineWidth', 2);
title('Internal Temperature Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);
ylabel('Temperature (^\circ C)','fontsize',10);

%% Temp Outside
temp_outside_v = data(:, 3);

%data points
temp_outside_i = 22.2; %(Degrees C)
temp_outside_v_i = 3.14;
temp_outside_f = -40; %Not real
temp_outside_v_f = 2.35;
%slope and y intercept
temp_outside_slope = (temp_outside_v_f - temp_outside_v_i) / (temp_outside_f - temp_outside_i);
temp_outside_int = temp_outside_v_i - (temp_outside_slope * temp_outside_i);


temp_outside_range = [-55:150];
figure();
plot(temp_outside_range, (temp_outside_slope .* temp_outside_range) + temp_outside_int, 'LineWidth', 2);
axis ([temp_outside_range(1) temp_outside_range(end) v_range]);
title('External Temperature Calibration Curve','fontsize',14);
xlabel('Temperature (^\circ C)','fontsize',10);
ylabel('Voltage (V)','fontsize',10);


cal_temp_outside = (temp_outside_v - temp_outside_int) ./ temp_outside_slope;
cal_temp_outside_filt = cal_temp_outside;

for x = 1 : 10;
    cal_temp_outside_filt = sgolayfilt(cal_temp_outside_filt, 2, 19);
end

figure();
plot(time_min, cal_temp_outside_filt, 'LineWidth', 2);
title('External Temperature Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);
ylabel('Temperature (^\circ C)','fontsize',10);

%% Both temp
figure();
hold on;
plot(time_min, cal_temp_filt, 'LineWidth', 2);
plot(time_min, cal_temp_outside_filt, 'LineWidth', 2);
title('Temperature Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);
ylabel('Temperature (^\circ C)','fontsize',10);
legend('Internal', 'External')
%% PRESSURE

pres_v = data(:, 4);

%data points
pres_i = 0;
pres_v_i = 0;
pres_f = 29.62;
pres_v_f = 3.97;
%slope and y intercept
pres_slope = (pres_v_f - pres_v_i) / (pres_f - pres_i);
pres_int = pres_v_i - (pres_slope * pres_i);


pres_range = [0:40];
figure();
plot(pres_range, (pres_slope .* pres_range) + pres_int, 'LineWidth', 2);
axis ([pres_range(1) pres_range(end) v_range]);
title('Pressure Calibration Curve','fontsize',14);
xlabel('Pressure (inMg)','fontsize',10);
ylabel('Voltage (V)','fontsize',10);


cal_pres = (pres_v - pres_int) ./ pres_slope;
cal_pres_filt = cal_pres;

for x = 1 : 10;
    cal_pres_filt = sgolayfilt(cal_pres_filt, 2, 19);
end

figure();
plot(time_min, cal_pres_filt, 'LineWidth', 2);
title('Pressure Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);
ylabel('Pressure (inMg)','fontsize',10);
%% Acceleration x

ax_v = data(:, 5);

%data points
ax_i = -1;
ax_v_i = 1.52;
ax_f = 1;
ax_v_f = 1.81;
%slope and y intercept
ax_slope = (ax_v_f - ax_v_i) / (ax_f - ax_i);
ax_int = ax_v_i - (ax_slope * ax_i);

cal_ax = (ax_v - ax_int) ./ ax_slope;
cal_ax_filt = cal_ax;

for x = 1 : 10;
    cal_ax_filt = sgolayfilt(cal_ax_filt, 2, 19);
end

%% Acceleration Y

ay_v = data(:, 6);

%data points
ay_i = -1;
ay_v_i = 1.63;
ay_f = 1;
ay_v_f = 1.83;
%slope and y intercept
ay_slope = (ay_v_f - ay_v_i) / (ay_f - ay_i);
ay_int = ay_v_i - (ay_slope * ay_i);

cal_ay = (ay_v - ay_int) ./ ay_slope;
cal_ay_filt = cal_ay;

for x = 1 : 10;
    cal_ay_filt = sgolayfilt(cal_ay_filt, 2, 19);
end

%% Acceleration Z

az_v = data(:, 7);

%data points
az_i = -1;
az_v_i = 1.58;
az_f = 1;
az_v_f = 1.78;
%slope and y intercept
az_slope = (az_v_f - az_v_i) / (az_f - az_i);
az_int = az_v_i - (az_slope * az_i);


az_range = [-10:10];
figure();
hold on;
plot(az_range, (ax_slope .* az_range) + ax_int, 'LineWidth', 2);
plot(az_range, (ay_slope .* az_range) + ay_int, 'LineWidth', 2);
plot(az_range, (az_slope .* az_range) + az_int, 'LineWidth', 2);
axis ([az_range(1) az_range(end) v_range]);
title('Acceleration Calibration Curve','fontsize',14);
xlabel('Acceleration (g)','fontsize',10);
ylabel('Voltage (V)','fontsize',10);
legend('X', 'Y', 'Z', 'location', 'northeast');

cal_az = (az_v - az_int) ./ az_slope;
cal_az_filt = cal_az;

for x = 1 : 10;
    cal_az_filt = sgolayfilt(cal_az_filt, 2, 19);
end

figure();
hold on;
plot(time_min, cal_ax_filt, 'LineWidth', 2);
plot(time_min, cal_ay_filt, 'LineWidth', 2);
plot(time_min, cal_az_filt, 'LineWidth', 2);
title('Acceleration Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);
ylabel('Acceleration (g)','fontsize',10);
legend('X', 'Y', 'Z', 'location', 'southwest');
%% Battery

bat_v = data(:, 8);
funcbat_v = funcdata(:, 8);
funcbat_v = funcbat_v(1:length(time_min), :);


cal_bat_filt = 2 .* bat_v;
cal_funcbat_filt = 2 .* funcbat_v;

for x = 1 : 10;
    cal_bat_filt = sgolayfilt(cal_bat_filt, 2, 19);
end

for x = 1 : 10;
    cal_funcbat_filt = sgolayfilt(cal_funcbat_filt, 2, 19);
end

figure();
hold on;
title('Analysis of Battery Voltage Over Time','fontsize',14);
xlabel('Time (min)','fontsize',10);

yyaxis right;
plot(time_min, cal_temp_filt, 'LineWidth', 2);
ylabel('Temperature (^\circ C)','fontsize',10);
ylim([-20 20]);

yyaxis left;
plot(time_min, cal_bat_filt, 'LineWidth', 2);
plot(time_min, cal_funcbat_filt, 'LineWidth', 2);
ylim([0 8.5]);
ylabel('Voltage (V)','fontsize',10);

legend('Balloon Launch Voltage', 'Functional Test Voltage', 'Balloon Launch Internal Temperature', 'location', 'southeast')