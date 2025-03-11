from utilis import *
import cv2

w,h = 360,240
pid = [0.5,0.5,0]
pError = 0
startCounter = 0

drone = initializeTello()


while True:

    if startCounter == 0:
        drone.takeoff()
        drone.move_up(30)
        startCounter = 1

    img = telloGetFrame(drone, w, h)

    img, info = findFace(img)

    pError = trackFace(drone, info, w, pid, pError)
    print(info[0][0])

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break