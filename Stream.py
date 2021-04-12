import cv2
from utils import Rotate

cap = cv2.VideoCapture("http://172.30.1.25:8091/?action=stream")

while(cap.isOpened()):
    ret, frame = cap.read()
    Rotate(frame, 90)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 :
        break;
cap.release()
cv2.destroyAllWindows()