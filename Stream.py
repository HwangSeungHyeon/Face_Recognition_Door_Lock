import cv2

# 스트림이 제대로 열리는지 확인하는 코드

cap = cv2.VideoCapture("http://172.30.1.25:8091/?action=stream")

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 :
        break;
cap.release()
cv2.destroyAllWindows()