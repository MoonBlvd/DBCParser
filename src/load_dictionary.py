import numpy as np
import pickle
import matplotlib.pyplot as plt
import csv
import sys

def load_dictionary(fileName):
    data = pickle.load(open(fileName, 'rb'))
    return data
if __name__ == '__main__':
    fileName = sys.argv[1]
    #filePath = '../translated_data/05182017/'
    filePath = '../translated_data/06172017/'
    data = load_dictionary(filePath + fileName + '.pkl')
    lenData =  len(data)
    vehicleSpeed = []
    time464 = []
    engineSpeed2 = []
    time476 = []
    brake = []
    accelPedal = []
    time380 = []
    TSRList = [1824,1825,1826,1827,1828,1829,1830]
    TSR1Position = []
    TSR1Type = []
    timeTSR1 = []
    ObstacleListA = [1849,1852,1855,1858]
    ObstacleListB = [1850,1853,1856,1859]
    ObstacleListC = [1851,1854,1857,1860]
    ObstaclePosition = []
    ObstacleID = []
    ObstacleType = []
    ObstacleBrake = []
    ObstacleVelX = []
    ObstacleStatus = []
    ObstacleTime = []
    ObstacleSize = []
    ObstacleLane = []
    ObstacleAge = []
    ObstacleAccelX = []
    ObstacleAngle = []
    LaneTime = []
    LaneTypes = []
    LaneConfs = []
    LaneDists = []
    LeftLaneHeadings = []
    RightLaneHeadings = []
    LeftLaneCurvatures = []
    RightLaneCurvatures = []
    Curvatures = []
    LeftLaneCurvaturesDerivative = []
    RightLaneCurvaturesDerivative = []
    LeftLanePosition = []
    RightLanePosition = []
    CarTime = []
    Speeds = []
    YawAngles = []
    PitchAngles = []
    Brakes = []
    Blinks = []
    Beams = []
    Wippers = []
    for i in range(lenData):
        if data[i]['msgID'] == 464:
            vehicleSpeed.append(data[i]['VehicleSpeed'])
            time464.append(data[i]['Time'])
        if data[i]['msgID'] == 476:
            engineSpeed2.append(data[i]['EngineSpeed2'])
            time476.append(data[i]['Time'])
        if data[i]['msgID'] == 380:
            brake.append(data[i]['Brake'])
            accelPedal.append(data[i]['AccPedal']/100)
            time380.append(data[i]['Time'])
        # Traffic Signs
        if data[i]['msgID'] in TSRList:
            TSR1Position.append(np.array([ \
                    data[i]['Sign_pos_X'], \
                    data[i]['Sign_pos_Y'], \
                    data[i]['Sign_pos_Z']]))
            TSR1Type.append(data[i]['vision_only_sign_type'])
            timeTSR1.append(data[i]['Time'])
        # Obstacles
        if data[i]['msgID'] in ObstacleListA:
            ObstaclePosition.append(np.array([ \
                    data[i]['Obstacle_Pos_X'], \
                    data[i]['Obstacle_Pos_Y']]))
            ObstacleType.append(data[i]['Obstacle_Type'])
            ObstacleID.append(data[i]['Obstacle_ID'])
            ObstacleBrake.append(data[i]['Obstacle_Brake_Lights'])
            ObstacleVelX.append(data[i]['Obstacle_Rel_Vel_X'])
            ObstacleStatus.append(data[i]['Obstacle_Status'])
            ObstacleTime.append(data[i]['Time'])
        if data[i]['msgID'] in ObstacleListB:
            ObstacleSize.append(np.array([ \
                    data[i]['Obstacle_Width'], \
                    data[i]['Obstacle_Length']]))
            ObstacleLane.append(data[i]['Obstacle_Lane'])
            ObstacleAge.append(data[i]['Obstacle_Age'])
        if data[i]['msgID'] in ObstacleListC:
            ObstacleAccelX.append(data[i]['Object_Accel_X'])
            ObstacleAngle.append(data[i]['Obstacle_Angle'])
        # Lanes
        if data[i]['msgID'] == 1641:
            LaneTime.append(data[i]['Time'])
            LaneTypes.append(np.array([data[i]['Lane_type_right'], data[i]['Lane_type_left']]))
            LaneConfs.append(np.array([data[i]['Lane_conf_right'], data[i]['Lane_conf_left']]))
            LaneDists.append(np.array([data[i]['distance_to_lane_R'], data[i]['distance_to_lane_L']]))
        # Car signals from Mobileye
        if data[i]['msgID'] == 1888:
            CarTime.append(data[i]['Time'])
            Speeds.append(data[i]['speed'])
            Brakes.append(data[i]['Brakes'])
            Beams.append(np.array([data[i]['HighBeam'], data[i]['LowBeam']]))
            Blinks.append(np.array([data[i]['right_blink'],data[i]['Left_blink']]))
            Wippers.append(data[i]['wippers'])
        if data[i]['msgID'] == 1847:
            YawAngles.append(data[i]['Yaw_Angle'])
            PitchAngles.append(data[i]['Pitch_Angle'])
            Curvatures.append(data[i]['Lane_Curvature'])
        if data[i]['msgID'] == 1894:
            LeftLaneCurvatures.append(data[i]['Curvature'])
            LeftLaneCurvaturesDerivative.append(data[i]['Curvature_Derivative'])
            LeftLanePosition.append(data[i]['Position'])
        if data[i]['msgID'] == 1896:
            RightLaneCurvatures.append(data[i]['Curvature'])
            RightLaneCurvaturesDerivative.append(data[i]['Curvature_Derivative'])
            RightLanePosition.append(data[i]['Position'])
        if data[i]['msgID'] == 1895:
            LeftLaneHeadings.append(data[i]['Heading_Angle'])
        if data[i]['msgID'] == 1897:
            RightLaneHeadings.append(data[i]['Heading_Angle'])
    '''
    # save type and position and time of trafficsign_1
    with open(filePath + fileName + '_TSR_1.csv', 'w') as csvfile:
        fieldsNames = ['Time','TSR type', 'Pos_X', 'Pos_Y', 'Pos_Z']
        writer = csv.DictWriter(csvfile, fieldsNames)
        writer.writeheader()
        for i in range(len(timeTSR1)):
            writer.writerow({'Time': timeTSR1[i], \
                             'TSR type': TSR1Type[i], \
                             'Pos_X': TSR1Position[i][0], \
                             'Pos_Y': TSR1Position[i][1], \
                             'Pos_Z': TSR1Position[i][2]})
    with open(filePath + fileName + '_obstacles.csv', 'w') as csvfile:
        fieldsNames = ['Time','Obstacle_ID','Obstacle_Type', 'Obstacle_Age', 'Obstacle_Status','Obstacle_X',\
                       'Obstacle_Y','Obstacle_Lane','Obstacle_Width','Obstacle_Length','Obstacle_Brake',\
                       'Obstacle_Vel_X','Obstacle_Accel_X','Obstacle_Angle']
        writer = csv.DictWriter(csvfile, fieldsNames)
        writer.writeheader()
        for i in range(len(ObstacleTime)):
            writer.writerow({'Time': ObstacleTime[i], \
            	             'Obstacle_ID': ObstacleID[i], \
                             'Obstacle_Type': ObstacleType[i], \
                             'Obstacle_Age': ObstacleAge[i], \
                             'Obstacle_Status': ObstacleStatus[i], \
                             'Obstacle_X': ObstaclePosition[i][0], \
                             'Obstacle_Y': ObstaclePosition[i][1], \
                             'Obstacle_Lane': ObstacleLane[i], \
                             'Obstacle_Width': ObstacleSize[i][0], \
                             'Obstacle_Length': ObstacleSize[i][1], \
                             'Obstacle_Brake': ObstacleBrake[i], \
                             'Obstacle_Vel_X': ObstacleVelX[i], \
                             'Obstacle_Accel_X': ObstacleAccelX[i], \
                             'Obstacle_Angle': ObstacleAngle[i]})
    with open(filePath + fileName+'_lanes.csv', 'w') as csvfile:
        fieldsNames = ['Time','Lane_type_right', 'Lane_type_left', 'Lane_conf_right', 'Lane_conf_left', \
                       'Lane_dist_right', 'Lane_dist_left', 'Lane_heading_right', 'Lane_heading_left', \
                       'Lane_curvature_right', 'Lane_curvature_left', 'Lane_curvature', \
                       'Lane_curvature_derivative_right','Lane_curvature_derivative_left',\
                       'Lane_position_right', 'Lane_position_left']
        writer = csv.DictWriter(csvfile, fieldsNames)
        writer.writeheader()
        for i in range(len(LaneTime)):
            writer.writerow({'Time': LaneTime[i], \
                             'Lane_type_right': LaneTypes[i][0], \
                             'Lane_type_left': LaneTypes[i][1], \
                             'Lane_conf_right': LaneConfs[i][0], \
                             'Lane_conf_left': LaneConfs[i][1], \
                             'Lane_dist_right': LaneDists[i][0], \
                             'Lane_dist_left': LaneDists[i][1], \
                             'Lane_heading_right': RightLaneHeadings[i], \
                             'Lane_heading_left': LeftLaneHeadings[i], \
                             'Lane_curvature_right': RightLaneCurvatures[i], \
                             'Lane_curvature_left': LeftLaneCurvatures[i], \
                             'Lane_curvature': Curvatures[i], \
                             'Lane_curvature_derivative_right':RightLaneCurvaturesDerivative[i], \
                             'Lane_curvature_derivative_left':LeftLaneCurvaturesDerivative[i], \
                             'Lane_position_right':RightLanePosition[i], \
                             'Lane_position_left':LeftLanePosition[i]})
    '''                         
    with open(filePath + fileName + '_carSignalFromMobileye.csv', 'w') as csvfile:
        fieldsNames = ['Time','Speeds', 'Yaw', 'Pitch', 'Brakes', 'Wippers', 'HighBeam', 'LowBeam','RightBlink','LeftBlink']
        writer = csv.DictWriter(csvfile, fieldsNames)
        writer.writeheader()
        for i in range(len(CarTime)):
            writer.writerow({'Time': CarTime[i], \
                             'Speeds': Speeds[i], \
                             'Yaw': YawAngles[i], \
                             'Pitch': PitchAngles[i], \
                             'Brakes': Brakes[i], \
                             'Wippers': Wippers[i], \
                             'HighBeam': Beams[i][0], \
                             'LowBeam': Beams[i][1],\
                             'RightBlink': Blinks[i][0],\
                             'LeftBlink': Blinks[i][1]})
'''
    plt.figure(1)
    plt.plot(time464, vehicleSpeed)
    plt.xlabel('Time [sec]')
    plt.ylabel('Vehicle speed [km/h]')
    plt.title('Vehicle speed')

    plt.figure(2)
    plt.plot(time476, engineSpeed2)
    plt.xlabel('Time [sec]')
    plt.ylabel('Engine speed [rpm]')
    plt.title('Engine speed')

    plt.figure(3)
    plots = [None]*2
    plots[0], = plt.plot(time380, brake, label = 'brake')
    plots[1], = plt.plot(time380, accelPedal, label = 'AccelPedal')
    plt.xlabel('Time [sec]')
    plt.ylabel('Value [ratio]')
    plt.title('Acceleration pedal and brake value')
    plt.legend(handles = plots)

    plt.show()
'''

    

