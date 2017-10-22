
clear all; clc;
%Start = 21000; % a piece of heading east trajectory
%End = 23000;
% plot(Start:End, new_yaw(Start:End))
% figure(2);plot(Start:End, NAV_vel(Start:End,1))
% figure(3);plot(Start:End, NAV_vel(Start:End,2))
% figure(4);plot(NAV_pos(Start:End,2), NAV_pos(Start:End,1))

%load data
filepath = 'Data_05182017/';
%filename = 'MIDG_Union_to_Lewisburg';
filename = 'MIDG';
data1 = load([filepath, filename, '.txt']);
time = (data1(:,3)-data1(1,3))*10e-4;
num_data = length(time);

temperature = data1(:,2);
accel = data1(:,7:9) * 10e-4 * 9.81 ; % m/s^2
NAV_pos = ecef2lla(data1(:,15:17));%.*[10e-7,10e-7,10e-2];% transfer to lat, long, alt
NAV_pos(:,1) = NAV_pos(:,1)+0.1897; % 0.1897 is the drift
NAV_vel = data1(:,18:20) * 10e-3; %V East, north, up, m/s
%[vx, vy, vz] = ecef2enu(data1(:,18), data1(:,19), data1(:,20), 0, 0, 0, referenceEllipsoid('wgs84'), 'radians');%*10e-2*3.6;% transfer to km/h
%NAV_vel = [vx,vy,vz];
%NAV_vel = NAV_vel * 10e-2*3.6;

GPS_pos = ecef2lla(data1(:,34:36));%*10e-7;
GPS_vel = data1(:,37:39) * 10e-3 * 3.6; % East north up
%[vx, vy, vz] = ecef2enu(data1(:,37), data1(:,38), data1(:,39), 0, 0, 0, referenceEllipsoid('wgs84'), 'radians');
%GPS_vel = [vx,vy,vz];
%GPS_vel = GPS_vel * 10e-2*3.6;

angle = data1(:,10:12) * (10e-3) * pi/180; % YAW, PITCH, ROLL, transferred to radians
yaw = angle(:,1);% +(pi/2 - mean(angle(Start:End,1))); % remove the yaw angle offset. 
pitch = angle(:,2);
roll = angle(:,3);
for i = 1:length(yaw)
    if yaw(i) > pi
        yaw(i) = yaw(i) - 2*pi;
    elseif yaw(i) < -pi
            yaw(i) = yaw(i) + 2*pi;
    end
end
PQR_vel = data1(:,4:6) * (10e-3) * pi/180; % transferred to radians/sec

window_size = 2;
start = 6064; % try to match with MOBILEYE
%start = 1; % 
positions = [];
velocities = [];
yaws = [];
pitchs = [];
rolls = [];
PQRs = [];
accels = [];
i = start;
downsample_time = [];
data = [];


while i <= length(time)
    
    if i+window_size-1 <= num_data
        tmp_pos = mean(NAV_pos(i:i+window_size-1, :),1);
        tmp_vel = mean(NAV_vel(i:i+window_size-1, :),1);
        tmp_yaw = mean(yaw(i:i+window_size-1));
        tmp_pitch = mean(pitch(i:i+window_size-1));
        tmp_roll = mean(roll(i:i+window_size-1));
        tmp_PQR = mean(PQR_vel(i:i+window_size-1, :),1);
        tmp_accel = mean(accel(i:i+window_size-1, :),1);
    else
        tmp_pos = mean(NAV_pos(i:end, :),1);
        tmp_vel = mean(NAV_vel(i:end, :),1);
        tmp_yaw = mean(yaw(i:end));
        tmp_pitch = mean(pitch(i:end));
        tmp_roll = mean(roll(i:end));
        tmp_PQR = mean(PQR_vel(i:end, :),1);
        tmp_accel = mean(accel(i:end, :),1);
    end
    positions = [positions;tmp_pos];
    velocities = [velocities;tmp_vel];
    yaws = [yaws; tmp_yaw];
    pitchs = [pitchs; tmp_pitch];
    rolls = [rolls; tmp_roll];
    PQRs = [PQRs; tmp_PQR];
    accels = [accels; tmp_accel];
    downsample_time = [downsample_time; time(i) - time(start)];
    
    data = [data; [time(i)- time(start), tmp_pos(1:2), tmp_yaw, tmp_pitch, tmp_roll, tmp_vel(1:3), tmp_accel(1:3), tmp_PQR]]; % yaw[rad], pitch, roll, v_east[m/s], v_north, a_x[m/s^2],a_y, a_z, P[rad/s], Q, R
    i = i+window_size;

end
Start = 1;%10089;
End = 10170;
%Start = 1;%10739;
%End = 10730;%10783;
%plot(positions(Start:End,2), positions(Start:End,1));

%% plot distribution
%plot(data(:,3), data(:,4),'*');

%% save data
format long
data = data;

csvwrite([filepath,filename,'.csv'], data,'precision', '%.6f');
%long_vel = velocities(:,2) .* cos(yaws) + velocities(:,1) .* sin(yaws);
%lat_vel = velocities(:,2) .* sin(yaws) - velocities(:,1) .* cos(yaws);
% plot(NAV_pos(:,2), NAV_pos(:,1), 'b');
% hold on;
% plot(GPS_pos(:,2), GPS_pos(:,1), 'r');
% hold on;
% plot(GPS_pos(1,2), GPS_pos(1,1), 'kp','MarkerSize',10);
% %set(gca,'color','none');
% axis off;
% axis equal

% % save transparent figures
% A1=imread('MIDG_trajectory.png');
% D=ones(size(A1(:,:,1)));
% D(all(A1==255,3)) = 0;
% imwrite(A1,'MIDG_trajectory.png','Alpha',D);

% plot velocities
% colors = ['r','g','b'];
% compose_vel = sqrt(NAV_vel(:,1).^2 + NAV_vel(:,2).^2); 
% for i = 1:3
%     plot(time, NAV_vel(:,i),colors(i), 'LineWidth', 2);hold on;
%     plot(time, GPS_vel(:,i),'k--');hold on;
% end
% figure(2)
% plot(time, compose_vel,'LineWidth',2); hold on;


% % plot accel
% colors = ['r','g','b'];
% % reduce steady state error
% accel = accel - mean(accel(1:100,:));
% for i = 1:3
%     plot(time, accel(:,i),colors(i), 'LineWidth', 2);hold on;
% end

% %plot angular vel
% colors = ['r','g','b'];
% % reduce steady state error
% angle_vel = angle_vel - mean(angle_vel(1:100,:));
% for i = 1:3
%     plot(time, angle_vel(:,i),colors(i), 'LineWidth', 2);hold on;
% end



%------------------------------------------------------------------------------------------------------------------
% % load Mia's data
% format long
% filename2 = 'Mia_GPS_Data.txt';
% data2 = csvread(filename2);
% time2 =  data2(:,1) - data2(1,1);
% long = data2(:,2);lat = data2(:,3);alt = data2(:,4);
% accuracy = data2(:,5); bearing = data2(:,6); speed = data2(:,7);


% figure(3)
% plot(long,lat,'r');hold on;
% plot(long(1),lat(1),'kp','MarkerSize',10);
% axis off;
% axis equal

% % Store strings of long and lat coordinates
% strFile = {};
% for i = 1:length(time2)
%      str = ['{lat: ' num2str(lat(i))   ',lng: '   num2str(long(i))  '},'];
%      strFile{i} = str;
% end
