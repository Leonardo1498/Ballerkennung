def ballerkennung():
    BILDBREITE = 640
    BILDHOEHE = 480
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    import numpy as np
    import cv2
    import imutils
    capture = cv2.VideoCapture(1)
    print(capture.isOpened())
    capture.set(3, BILDBREITE)
    capture.set(4, BILDHOEHE)
   # while capture.isOpened:
    for i in range(10):
        success, frame = capture.read()
        orangeLower = (0, 120, 120)
        orangeUpper = (15, 255, 255)
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, orangeLower, orangeUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                distance_to_center = BILDBREITE/2 - center[0]
                return radius,distance_to_center
                #cv2.circle(frame, center, 5, (0, 0, 255), -1)

        try:
            object_height = radius * 2
            test = str(radius)
        except UnboundLocalError:
            test = "Gibt es nicht"


        #distance = distance_to_object(0,9,BILDHOEHE,object_height,0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (0, 100)
        fontScale = 1
        fontColor = (0, 0, 255)
        thickness = 1
        lineType = 2

        cv2.putText(frame, test,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
        if success == True:
            cv2.startWindowThread()
            cv2.namedWindow("Vorschau")
            cv2.imshow("Webcam Video",frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    capture.release()

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Wichtig f??r Macintosh

    return None,None

def distance_to_object(brennweite,reele_hoehe,bildhoehe,objekthoehe,sensorhoehe):
    pass



if __name__=='__main__':
    ballerkennung()