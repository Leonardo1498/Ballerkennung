import matplotlib.pyplot as plt


def ballerkennung():
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    import numpy as np
    import cv2
    import imutils
    capture = cv2.VideoCapture(0)
    print(capture.isOpened())
    capture.set(3, 640)
    capture.set(4, 480)

    while capture.isOpened:
        success, frame = capture.read()
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        farbe = farberkennung(frame)
        canny = test_canny(farbe)
        output = draw_rect(canny)

        #erkennung = template(gray)
        if success == True:
            cv2.startWindowThread()
            cv2.namedWindow("Vorschau")
            cv2.imshow("Webcam Video",canny)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    capture.release()

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Wichtig für Macintosh
def test_canny(img):
    import cv2
    threshold_1 = 150
    threshold_2 = 300
    canny = cv2.Canny(img, threshold_1, threshold_2)
    return canny
def farberkennung(img):
    import cv2
    import numpy as np
    #range =  ([0,0,128],[64,200,255])
    range = ([0, 0, 0], [255, 255, 255])
    lowerRange = np.array(range[0])
    upperRange = np.array(range[1])
    mask = cv2.inRange(img,lowerRange,upperRange)
    output = cv2.bitwise_and(img, img, mask=mask)
    return output
def draw_rect(img):
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    import numpy as np
    import cv2
    import imutils
    cnts,hierachy = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print(len(cnts))
    #cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    output = cv2.minAreaRect(c)
    return output
    #else:
        #return img
if __name__ == '__main__':
    ballerkennung()

