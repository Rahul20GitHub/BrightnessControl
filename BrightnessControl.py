import cv2
import screen_brightness_control as sbc
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.75)
tipIds = [4,8,12,16,20]
bri = [0,20,40,60,80,100]
while True:
    success, img  = cap.read()
    img = detector.findHands(img)
    img = cv2.flip(img,1)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers = fingers.count(1)

        #Brightness Controll
        if totalFingers == 5:
            sbc.set_brightness(bri[5], display=0)
            dis = bri[5]
        elif totalFingers == 4:
            sbc.set_brightness(bri[4], display=0)
            dis = bri[4]
        elif totalFingers == 3:
            sbc.set_brightness(bri[3], display=0)
            dis = bri[3]
        elif totalFingers == 2:
            sbc.set_brightness(bri[2], display=0)
            dis = bri[2]
        elif totalFingers == 1:
            sbc.set_brightness(bri[1], display=0)
            dis = bri[1]
        else:
            sbc.set_brightness(bri[0], display=0)
            dis = bri[0]

        cv2.putText(img, "Brighthess: " + str(dis), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(255,255,255),2)
    cv2.imshow("Image", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

