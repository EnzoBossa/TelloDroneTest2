import numpy as np
from djitellopy import Tello
import cv2

def initializeTello():
    drone = Tello()
    drone.connect()
    drone.for_back_velocity = 0
    drone.left_right_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.speed = 0

    print(drone.get_battery())
    drone.streamoff()
    drone.streamon()
    return drone


def telloGetFrame(drone, w=360, h=240):
    myFrame = drone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w,h))
    return img

def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,4)

    myFaceListCenter = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h),(0,0,255), 2)

        #Finding area and center of face

        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListCenter.append([cx,cy])

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListCenter[i],myFaceListArea[i]]   #only returning the area of the closest face
    else:
        return img, [[0,0],0]

def trackFace(drone, info, w, pid, pError):

    #PID controller yaw speed
    error = info[0][0] - w//2
    speed = pid[0]*error + pid[1]*(error-pError)
    speed = int(np.clip(speed, -100, 100)) #limiting the speed between accepted values
    print(speed)


    if info[0][0] != 0:
        drone.yaw_velocity = speed
    else:
        drone.for_back_velocity = 0
        drone.left_right_velocity = 0
        drone.up_down_velocity = 0
        drone.yaw_velocity = 0
        error = 0

    if drone.send_rc_control:
        drone.send_rc_control(drone.left_right_velocity, drone.for_back_velocity,
                              drone.up_down_velocity, drone.yaw_velocity)



    return error