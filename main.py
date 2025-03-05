import cv2 
from HandTrackModule import handDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0) 
cap.set(3, 1880)
cap.set(4, 720)

detector = handDetector(maxHands=1)
keys = [['1','2','3','4','5','6','7','8','9','0'],
        ['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L','Ñ'],
        ['Z','X','C','V','B','N','M',',','.','/']]

finalText = ""

keyboard = Controller()

def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),thickness=1)
        cv2.putText(img,button.text,(x+10, y+30)
                    ,cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),5)
    return img

class button():
    def __init__(self,pos,text,size=[40,40]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []

for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(button([x*50+90,50*i+50],key))

def virtKeyboard():
    while True:
        succes, img = cap.read()
        img = detector.findHands(img)
        lmlist,bboxInfo = detector.findPosition(img)
        img = drawALL(img,buttonList)

        if lmlist:
            for button in buttonList:
                x,y = button.pos
                w,h = button.size

                if x<lmlist[8][1]<x+w and y<lmlist[8][2]<y+h:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=3)
                    cv2.putText(img,button.text,(x+10, y+30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),5)
                    l,_,_ = detector.findDistance(8,12,img)
                    #print(l)

                    #when click
                    if l<40:
                        keyboard.press(button.text)
                        cv2.rectangle(img,(x,y),(x+w,y+h),(215,200,0),thickness=1)
                        cv2.putText(img,button.text,(x+10, y+30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),5)
                        finalText += button.text
                        sleep(0.15)

        cv2.rectangle(img,(50,350),(500,450),(175,175,0),thickness=3)
        cv2.putText(img,finalText,(60, 425),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),5)

        cv2.imshow('img',img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
  virtKeyboard()
