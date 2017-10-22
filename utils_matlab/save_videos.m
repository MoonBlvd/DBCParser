function save_videos(Frames, num_videos)
%     start = 757;
% 
%     video = VideoWriter('Mobileye_detection_0.avi');
%     open(video);
%     writeVideo(video, Frames(1:start-1));
%     close(video);

%     for i = 1:27
%         video = VideoWriter(['Mobileye_detection_', num2str(i), '.avi']);
%         open(video);
%         writeVideo(video, Frames(start:start+1000));
%         close(video);
%         start = start + 1001;
%     end
% 
%     video = VideoWriter('Mobileye_detection_28.avi');
%     open(video);
%     writeVideo(video, Frames(start:27914));
%     close(video);
    
    
    video = VideoWriter(['Mobileye_detection_', num2str(num_videos), '.avi']);
    open(video);
    writeVideo(video, Frames);
    close(video);
end