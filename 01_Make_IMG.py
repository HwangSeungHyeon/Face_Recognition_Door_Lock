from imutils.video import VideoStream
import time, os
import cv2

cascade = "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(cascade)

def face_detect(img):
    #흑백처리 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #얼굴 찾기 
    faces = detector.detectMultiScale(gray,1.3,5)

    #찾은 얼굴이 없으면 False 리턴
    if faces is():
        return False

    #얼굴이 있으면 True 리턴
    for(x,y,w,h) in faces:
        return True


print("유저 이름: ")
people_name = input()

save_path = "known_people/" + people_name +"/"
print("저장할 폴더의 경로는 " + save_path + " 입니다.")

if os.path.isdir(save_path)==False:
    os.mkdir(save_path)

vs = VideoStream(src=0).start()
time.sleep(2.0)

cnt = 0

while True:
    frame = vs.read()
    cv2.imshow("Frame", frame)

    if cnt is 0:
        print("얼굴 사진을 찍습니다.")

    # 얼굴이 존재할 경우 5장의 사진을 저장
    if face_detect(frame) is not False and cnt < 5:
        img_name = str(cnt) + ".jpg"
        cv2.imwrite(save_path + "/" + img_name, frame)
        print("[Info] Capture the image: " + img_name)
        cnt2 = cnt
        cnt += 1

        if cnt2 is 4:
            print("얼굴 사진을 다 모았습니다. q를 누르면 종료합니다.")

    else:
        pass

    key = cv2.waitKey(1) & 0xFF

    # q를 누를 경우 루프 종료
    if key == ord("q"):
    	break

cv2.destroyAllWindows()
vs.stop()