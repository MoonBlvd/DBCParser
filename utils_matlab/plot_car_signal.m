function plot_car_signal(car_signal, obstacle, lane, TSR, MIDG, name)
    subplot(4,1,1)
    plot(car_signal.time,car_signal.speed/1.60934);
    title(name);
    xlabel('Time [seconds]');ylabel('speed [mph]');
    set(gca,'fontsize',18)
    
    subplot(4,1,2)
    plot(lane.time,lane.right_curvature);
    xlabel('Time [seconds]');ylabel('right curvature');
    set(gca,'fontsize',18)
    
    subplot(4,1,3)
    plot(lane.time,lane.left_curvature);
    xlabel('Time [seconds]');ylabel('left curvature');
    set(gca,'fontsize',18)
    
    
end