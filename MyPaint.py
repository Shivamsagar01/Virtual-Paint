import cv2
import numpy as np
import mediapipe as mp
import os

# ============adding menu bar===========
folderpath = "titlemenu"
mylist = os.listdir(folderpath)
print(mylist)
overlaylist = []

for impath in mylist:
    image = cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
# ======================================
imgtag = cv2.imread("Resources/BottomTag.png")
whitepage = cv2.imread("Resources/Virtual Paint Canvas.png")

# ==========Initial values===============
header = overlaylist[0]
brushthickness = 20
eraserthickness = 20
drawcolor = (0,0,255)
xp,yp = 0,0
count = 1
# ======================================

# ============hand detection============
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
# ======================================


canvas = np.zeros((720,1280,3),np.uint8)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1280)
cap.set(10,100)



def findhandlandmarks(imgRGB):   # function to track Hand
    results = hands.process(imgRGB)
    lmlist = []
    if results.multi_hand_landmarks:
        for handlams in results.multi_hand_landmarks:
            for id, lm in enumerate(handlams.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handlams, mpHands.HAND_CONNECTIONS)
    return lmlist



while True:
    # import webcam
    s,img = cap.read()
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # find hand landmarks
    lmlist = findhandlandmarks(imgRGB)

    if (len(lmlist)) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        # print(lmlist)
        if lmlist[8][2] < lmlist[6][2] and lmlist[12][2] > lmlist[10][2]:
            print("drawing mode")
            cv2.circle(img, (x1, y1), 10, drawcolor, cv2.FILLED)
            if y1>127:
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                if drawcolor == (0, 0, 0):
                    eraserthickness = 50
                    cv2.line(img, (xp, yp), (x1, y1), drawcolor, eraserthickness)
                    cv2.line(canvas, (xp, yp), (x1, y1), drawcolor, eraserthickness)
                    cv2.line(whitepage, (xp, yp), (x1, y1), (255,255,255), eraserthickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushthickness)
                    cv2.line(canvas, (xp, yp), (x1, y1), drawcolor, brushthickness)
                    cv2.line(whitepage, (xp, yp), (x1, y1), drawcolor, brushthickness)
                xp, yp = x1, y1



        elif lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2]:
            print("selection mode")
            xp, yp = 0, 0
            if y1<126:
                if 202 < x1 <372:
                    header = overlaylist[0]
                    drawcolor = (0,0,255)
                elif 399 < x1 < 580:
                    header = overlaylist[1]
                    drawcolor = (0,255,255)
                elif 601 < x1 < 792:
                    header = overlaylist[2]
                    drawcolor = (255,0,0)
                elif 822 < x1 < 1000:
                    header = overlaylist[3]
                    drawcolor = (0,255,0)
                elif 1027 < x1 < 1280:
                    header = overlaylist[4]
                    drawcolor = (0,0,0)
            cv2.circle(img, (x2 - 15, y2 - 15), 20, drawcolor, cv2.FILLED)

    imgGray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img, canvas)


    img[0:125, 0:1280] = header                     # adding the menu bar image
    img[648:720, 0:1280] = imgtag

    cv2.imshow("whitepage", whitepage)
    cv2.imshow("Video", img)


    key = cv2.waitKey(1)
    if key == ord('s'):           # to save drawing
        cv2.imwrite("Saved drawing/Drawing no_" + str(count)+".jpg",whitepage)
        count += 1

    elif key == ord('q'):           # to quit
        break

cap.release()
cv2.destroyAllWindows()