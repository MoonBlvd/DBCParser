function data_visualization()    
    clear all;clc;

    % %process obstacle data
    % path = '06192017/';
    % name = 'Union_to_Lewisburg';
    % obstacles = csvread([path, name, '_obstacles.csv']);
    % lanes = csvread([path, name,'_lanes.csv']);
    % traffic_signs = csvread([path, name,'_TSR_1.csv']);
    % CarSignalFromMobileye = csvread([path, name,'_carSignalFromMobileye.csv']);
    % MIDGs = csvread([path, 'MIDG_Union_to_Lewisburg.csv']);
    % name = '06/19/2017 data';

    % path = '06212017/';
    % name = 'A_to_B';
    % obstacles = csvread([path, name, '_obstacles.csv']);
    % lanes = csvread([path, name,'_lanes.csv']);
    % traffic_signs = csvread([path, name,'_TSR_1.csv']);
    % CarSignalFromMobileye = csvread([path, name,'_carSignalFromMobileye.csv']);
    % MIDGs = csvread([path, 'MIDG_A_to_D.csv']);
    % name = '06/21/2017 data'

    % %process obstacle data
    % path = '06212017/';
    % name = 'C_to_D';
    % obstacles = csvread([path, name, '_obstacles.csv']);
    % lanes = csvread([path, name,'_lanes.csv']);
    % traffic_signs = csvread([path, name,'_TSR_1.csv']);
    % CarSignalFromMobileye = csvread([path, name,'_carSignalFromMobileye.csv']);
    % MIDGs = csvread([path, 'MIDG_A_to_D.csv']);
    % name = '06/21/2017 data 2'

    file_path = '../translated_data/10172017/E_to_F_';
    name = '05/18/2017 data';
    obstacles = csvread([file_path, 'Obstacles.csv']); % Time	Obstacle_ID	Obstacle_Type	Obstacle_Age	Obstacle_Status	Obstacle_X	Obstacle_Y	Obstacle_Lane	Obstacle_Width	Obstacle_Length	Obstacle_Brake	Obstacle_Vel_X	Obstacle_Accel_X	Obstacle_Angle
    lanes = csvread([file_path, 'Lanes.csv']); % Time	Lane_type_right	Lane_type_left	Lane_conf_right	Lane_conf_left	Lane_dist_right	Lane_dist_left	Lane_heading_right	Lane_heading_left	Lane_curvature_right	Lane_curvature_left	Lane_curvature	Lane_curvature_derivative_right	Lane_curvature_derivative_left	Lane_position_right	Lane_position_left
    traffic_signs = csvread([file_path, 'TSR_1.csv']); % Time	TSR type	Pos_X	Pos_Y	Pos_Z
    CarSignalFromMobileye = csvread([file_path, 'CarSignalFromMobileye.csv']); % Time	Speeds	Yaw	Pitch	Brakes	Wippers	HighBeam	LowBeam	RightBlink	LeftBlink
    MIDGs = csvread([file_path, 'MIDG.csv']);

    global num_lanes lane_width car_w car_l freq range lane_length
    num_lanes = 3;
    lane_width = 4;
    car_w = 2;
    car_l = 5;
    freq = 11; %Hz
    range = [-30,30, -50,255];%lateral (y) limits and longitudinal (x) limits.
    lane_length = 20;
    % find the same_frame and different_frame by time interval threshold of
    % obstacle signal
    obstacles_time = obstacles(:,1);
    time_intervals = obstacles_time(2:end)-obstacles_time(1:end-1);
    same_frame = find(time_intervals < 1/freq)+1;
    different_frame = find(time_intervals > 1/freq)+1;

    num_data = size(CarSignalFromMobileye,1);
    %start = 5010;
    %start = 27000;
    start = 1;

    [car_signal, obstacle, lane, TSR, MIDG] = extract_structures(CarSignalFromMobileye, obstacles, lanes, traffic_signs, MIDGs);
    %plot_car_signal(car_signal, obstacle, lane, TSR, MIDG, name)

    %% fit gaussian 
    x = -0.1:0.005:0.1;
    %y = 1/sqrt(2*pi*var_pitch) * exp((-(x-m_pitch).^2)/(2*var_pitch));
    %plot(x,y,'-');

    % plot histogram
    % %histogram(car_signal.pitch);hold on;
    % pd = fitdist(MIDG.pitch, 'Normal');
    % y = pdf(pd, x);
    % %plot(x,y,'-');hold on;
    % %histfit(car_signal.pitch,20,'normal');
    % histfit(MIDG.roll,20,'normal');

    %% plot traffic
    k_obstacle = 1;k_TSR = 1;
    num_obstacles = 0;
    prev_time = 0;%car_signal.time(start-1);
    Frames = [];
    num_videos = 1;
    data_save = [];
    for i = start:num_data
        plot_obstacle_flag = false;
        plot_TSR_flag = false;
        num_obstacles = 0;
        num_TSR = 0;
        if i == start
            fig = figure(1);
        else
            clf(fig);
            fig = figure(1);
        end
        set(fig, 'Position', [100, 100, 300, 1000]);
        % plot lanes at this frame
        plot_lanes(lane, i);
        hold on;

        % plot ego car
        tmp = plot_one_obstacle(nan, k_obstacle, num_obstacles);
        hold on;

        % plot all obstacles detected at this frame
        while (k_obstacle <= length(obstacle.time)) && (car_signal.time(i) >= obstacle.time(k_obstacle) + 0.001) % if obstacles are detected, give 0.001 second threshol
            num_obstacles = num_obstacles + 1;
            obstacle_car = plot_one_obstacle(obstacle, k_obstacle, num_obstacles);hold on;
            k_obstacle = k_obstacle + 1;
        end

        % plot all traffic signs detected at this frame
        while (k_TSR <= length(TSR.time)) && (car_signal.time(i) >= TSR.time(k_TSR))
            num_TSR = num_TSR + 1;
            hold on;
            plot(TSR.y(k_TSR), TSR.x(k_TSR), 'ko','MarkerSize', 8, 'MarkerFaceColor','k');hold on;
            k_TSR = k_TSR + 1;
        end
        % add notations
        time_annotation = ['Time: ',num2str(car_signal.time(i)), ' [seconds]'];
        text(range(1),range(4)-5,time_annotation,'FontSize',16);
        idx_annotation = ['Index: ',num2str(i)];
        text(range(1),range(4)-15,idx_annotation,'FontSize',16);
        xlim(range(1:2));
        ylim(range(3:4));
        %pause(car_s ignal.time(i) - prev_time);

        % save videos
        Frames = [Frames,getframe(gcf)];
        if size(Frames,2) == 2000 || i == num_data
            save_videos(Frames, num_videos);
            Frames = [];
            num_videos = num_videos + 1;
        end
        hold off;
        prev_time = car_signal.time(i);
        data = [i, prev_time, num_obstacles, num_TSR, lane.right_type(i), lane.right_conf(i), lane.right_dist(i), lane.left_type(i), lane.left_conf(i), lane.left_dist(i)];
        data_save = [data_save; data];
        i
    end
    csvwrite('summary.csv', data_save);
    %save_videos(Frames);
    % video = VideoWriter('Mobileye_detection.avi');
    % open(video);
    % writeVideo(video, Frames);
    % close(video);
end

function [car_signal, obstacle, lane, TSR, MIDG] = extract_structures(CarSignalFromMobileye, obstacles, lanes, traffic_signs, MIDGs)
    global car_l    
    obstacle.time = obstacles(:,1);
    obstacle.ID = obstacles(:,2);
    obstacle.type = obstacles(:,3);
    obstacle.color = find_color(obstacle.type);
    obstacle.x = obstacles(:,6);
    obstacle.y = -obstacles(:,7);
    obstacle.w = obstacles(:,9);
    obstacle.l = obstacles(:,10);
    for i = 1:length(obstacle.l)
        if obstacle.l(i) == 31
            obstacle.l(i) = car_l;
        end
    end
    car_signal.time = CarSignalFromMobileye(:,1);
    car_signal.speed = CarSignalFromMobileye(:,2);
    car_signal.yaw = CarSignalFromMobileye(:,3);
    car_signal.pitch = CarSignalFromMobileye(:,4);
    car_signal.brake = CarSignalFromMobileye(:,5);
    car_signal.right_blink = CarSignalFromMobileye(:,9);
    car_signal.left_blink = CarSignalFromMobileye(:,10);
    
    lane.time = lanes(:,1);
    lane.right_type = lanes(:,2);
    lane.left_type = lanes(:,3);
    lane.right_conf = lanes(:,4);
    lane.left_conf = lanes(:,5);
    lane.right_dist = lanes(:,6);
    lane.left_dist = lanes(:,7);
    lane.right_heading = lanes(:,8);
    lane.left_heading = lanes(:,9);
    lane.right_curvature = lanes(:,10);
    lane.left_curvature = lanes(:,11);
    lane.right_curvature_derivative = lanes(:,13);
    lane.left_curvature_derivative = lanes(:,14);
    lane.right_position = lanes(:,15);
    lane.left_position = lanes(:,16);
    
    TSR.time = traffic_signs(:,1);
    TSR.type = traffic_signs(:,2);
    TSR.x = traffic_signs(:,3);
    TSR.y = traffic_signs(:,4);
    TSR.z = traffic_signs(:,5);
    
    if ~isempty(MIDGs)
        MIDG.yaw = MIDGs(:,2);
        MIDG.pitch = MIDGs(:,3);
        MIDG.roll = MIDGs(:,4);
        MIDG.v_east = MIDGs(:,5);
        MIDG.v_north = MIDGs(:,6);
        MIDG.accel_x = MIDGs(:,7);
        MIDG.accel_y = MIDGs(:,8);
        MIDG.accel_z = MIDGs(:,9);
        MIDG.P = MIDGs(:,10);
        MIDG.Q = MIDGs(:,11);
        MIDG.R = MIDGs(:,12);

    end
end

function plot_lanes(lane, i)
    % 
    % plot left lane
    
    if lane.left_conf(i) >= 1
        z = -5:0.1:20;
        C3 = lane.left_curvature_derivative(i);
        C2 = lane.left_curvature(i);
        C1 = lane.left_heading(i);
        C0 = lane.left_position(i);
        x = C3*z.^3 + C2*z.^2 + C1*z + C0;
        
        x_range = x;
        y_range = z;
        %x_range = [lane.left_dist(i), lane.left_dist(i)];
        %y_range = [0,lane_length];
        switch lane.left_type(i)
            case 0 % Dashed lane
                plot(x_range,y_range,'k--');
            case 1 % solid lane
                plot(x_range,y_range,'k-');
            %case 2 % None
            case 3 % Road edge
                plot(x_range,y_range,'k-','LaneWidth',3);
            case 4 % Double lanes
                plot(x_range,y_range,'k-');
                plot(x_range - 0.5,y_range,'k-');
            case 5 % Bott's dots
                plot(x_range,y_range,'k:');
            %case 6 % invalid    
        end
        hold on;
    end
    if lane.time(i) > 69.9
       aaa = 1234;
    end
    % plot right lane
    if lane.right_conf(i) >= 1
        z = -5:0.1:20;
        C3 = lane.right_curvature_derivative(i);
        C2 = lane.right_curvature(i);
        C1 = lane.right_heading(i);
        C0 = lane.right_position(i);
        x = C3*z.^3 + C2*z.^2 + C1*z + C0;
        
        x_range = x;
        y_range = z;
%         x_range = [lane.right_dist(i), lane.right_dist(i)];
%         y_range = [0,lane_length];
        switch lane.right_type(i)
            case 0 % Dashed lane
                plot(x_range,y_range,'k--');
            case 1 % solid lane
                plot(x_range,y_range,'k-');
            case 2 % None
                plot(x_range,y_range,'k--');
            case 3 % Road edge
                plot(x_range,y_range,'k-','LaneWidth',3);
            case 4 % Double lanes
                plot(x_range,y_range,'k-');
                plot(x_range + 0.5,y_range,'k-');
            case 5 % Bott's dots
                plot(x_range,y_range,'k:');
            %case 6 % invalid       
        end
        hold on;
    end
    if lane.time(i) > 69.9
       aaa = 1234;
    end
end

function obstacle_car = plot_one_obstacle(obstacle, k_obstacle, num_obstacles)
    global num_lanes lane_width car_w car_l range;
    
    obstacle_car = 0;
    if num_obstacles == 0
        % plot ego car
        rectangle('Position',[0 - car_w/2, 0 - car_l*2/3, car_w, car_l],'EdgeColor','r','FaceColor','r');
        
    elseif num_obstacles == 1
        % plot ego car
        %rectangle('Position',[0 - car_w/2, 0 - car_l*2/3, car_w, car_l],'EdgeColor','r','FaceColor','r');
        %xlim(range(1:2));
        %ylim(range(3:4));
        % plot the first obstacle car
        obstacle_car = rectangle('Position',[obstacle.y(k_obstacle)-obstacle.w(k_obstacle)/2, obstacle.x(k_obstacle),...
                                            obstacle.w(k_obstacle), obstacle.l(k_obstacle)],... %- obstacle.l/2
                                            'EdgeColor',obstacle.color(k_obstacle),'FaceColor',obstacle.color(k_obstacle));
    elseif num_obstacles > 1
        % plot the next obstacle car in this frame
        obstacle_car = rectangle('Position',[obstacle.y(k_obstacle)-obstacle.w(k_obstacle)/2, obstacle.x(k_obstacle),...
                                            obstacle.w(k_obstacle), obstacle.l(k_obstacle)],... %- obstacle.l/2
                                            'EdgeColor',obstacle.color(k_obstacle),'FaceColor',obstacle.color(k_obstacle));
    end
%     time_annotation = ['Time: ',num2str(obstacle.time(k_obstacle)), ' [seconds]'];
%     text(range(1),range(4)-5,time_annotation,'FontSize',16);
    
end

function color = find_color(type)
    len_type = length(type);
    color = [];
    for i = 1:len_type;
        if type(i) == 0 % car
            color = [color, 'b'];
        elseif type(i) == 1 %truck
            color = [color, 'k'];
        elseif type(i) == 2 % bike
            color = [color, 'g'];
        elseif type(i) == 3 % pedestrian
            color = [color, 'c'];
        elseif type(i) == 4 % bicycle
            color = [color, 'm'];
        else % everything else
            color = [color, 'b'];
        end
    end
end