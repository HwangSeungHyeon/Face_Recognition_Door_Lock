# -*- coding: utf-8 -*-

from imutils.video import VideoStream
from picamera import PiCamera, Color
from imutils import paths
import imutils
import time
import os
import cv2
import pickle
import numpy as np
import pandas as pd
import face_recognition
import RPi.GPIO as GPIO
from shutil import rmtree

def test():
    unlock()
    lock()

# 잠금을 해제하는 메소드
def unlock(pin = 18):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.cleanup(pin)
    time.sleep(5)
    
# 잠그는 메소드
def lock(pin = 18):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.cleanup(pin)
    time.sleep(1)

# 프레임을 회전시키는 메소드
def Rotate(src, degrees):
    if degrees == 90:
        dst = cv2.transpose(src)
        dst = cv2.flip(dst, 1)

    elif degrees == 180:
        dst = cv2.flip(src, -1)

    elif degrees == 270:
        dst = cv2.transpose(src)
        dst = cv2.flip(dst, 0)
    else:
        dst = None
    return dst

# 사진을 찍은 후 인코딩하는 메소드
def register():
    folder_dir = "/home/pi/Face_Recognition_Door_Lock/dataset/Known/"
    # 해당하는 폴더가 없을 경우 생성해줌
    if os.path.isdir(folder_dir)==False:
        os.mkdir(folder_dir)
        
    people_name = input("유저 이름: ")
    if people_name.find('Unknown') > -1 or people_name.find('unknown') > -1:
        print("[Info]: Can not using name 'unknown'")
        print("[Info] return the menu")
        pass
    
    else:
        save_path = folder_dir + people_name +"/"
        print("저장할 폴더의 경로는 " + save_path + " 입니다.")
    
        # 해당하는 폴더가 없을 경우 생성해줌
        if os.path.isdir(save_path)==False:
            os.mkdir(save_path)
        
        with PiCamera() as camera:
            camera.rotation = 90
            camera.annotate_text_size = 100
            camera.annotate_background = Color('red')
            camera.annotate_foreground = Color('yellow')
    
            camera.start_preview()
            camera.brightness = 50
            camera.exposure_mode = 'auto'
    
            for i in range(5, 0, -1):
                camera.annotate_text = str(i)
                time.sleep(1)
            camera.annotate_text = ""
        
            for i in range(10):
                time.sleep(0.5)
                camera.capture(save_path + people_name + '%s.jpg' %i)
            
            camera.annotate_text = "Finish!"
            time.sleep(2)
            camera.stop_preview()

            encodings_path = "/home/pi/Face_Recognition_Door_Lock/encoding/"
            if os.path.isdir(encodings_path)==False:
                os.mkdir(encodings_path)
        
            #datasets에 들어있는 이미지 list
            imagePaths = list(paths.list_images(save_path))
        
            #얼굴 embedding vector 데이터를 저장할 knownEncodings 리스트와, 학습한 얼굴 이름을 저장할 knownNames 리스트
            knownEncodings = []
            knownNames = []
        
            # dataset의 경로 상에 있는 이미지를 모두 가져옴
            for (i, imagePath) in enumerate(imagePaths):
                print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
                name = imagePath.split(os.path.sep)[-2]

                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
                # 얼굴의 박스 영역을 찾아줌
                boxes = face_recognition.face_locations(rgb, model = "hog")
            
                if not boxes:
                    print("[ERROR] Face does not detected")
                    pass
    
                # 박스 영역의 얼굴 임베딩 데이터를 추출
                encodings = face_recognition.face_encodings(rgb, boxes)
    
                # loop over the encodings
                for encoding in encodings:
                    knownEncodings.append(encoding)
                    knownNames.append(name)
                
            if not knownEncodings:
                print("[Error] Can't detect faces in all images")
            
            else:
                # 얼굴 임베딩 데이터와 이름을 pickle 파일로 저장
                print("[INFO] serializing encodings...")
                data = {"encodings": knownEncodings, "names": knownNames}

                with open(encodings_path + people_name + ".pkl", "wb") as f:
                    f.write(pickle.dumps(data))
                f.close()
            
                print("[Info] Delete images used for encoding")
                rmtree(save_path)

# 얼굴을 인식하는 메소드
def recognition():
    # pkl 데이터들을 합치는 부분
    base_dir = '/home/pi/Face_Recognition_Door_Lock/encoding/'
    if os.path.isdir(base_dir)==False:
        os.mkdir(base_dir)
        
    temp_encode = []
    temp_name = []
    
    for fname in os.listdir(base_dir):
        temp = pd.read_pickle(os.path.join(base_dir, fname))
        for e in temp["encodings"]: temp_encode.append(e)
        for n in temp["names"]: temp_name.append(n)

    data = {"encodings": temp_encode, "names": temp_name}
    print("[INFO] Successfully read Pickle File!")
    
    vs = VideoStream(usePiCamera=True).start()
    print("[Info] Camera Initialization")
    time.sleep(2.0)
    
    while True:
        frame = vs.read()
        frame = Rotate(frame, 90)
        frame = imutils.resize(frame, width = 300)
    
        # 도어락 제어 플래그
        flag = -1
        
        # 얼굴인식에 사용할 이미지
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 얼굴검출에 사용할 이미지
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #detected face
        boxes = face_recognition.face_locations(gray, model = "hog")

        # 검출한 얼굴 영역의 embedding vector를 생성
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # 카메라로 촬영중인 사람의 얼굴과 pickle 파일에 저장된 embedding vector를 비교
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance = 0.45)
            name = "Unknown"

            # 두 얼굴 사이의 거리를 비교
            face_distances = face_recognition.face_distance(data["encodings"], encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = data["names"][best_match_index]

            # 전혀 모르는 얼굴이면 name = "Unknown"
            # Unknown에 등록된 얼굴이면 name = Unknown
            # Known에 등록된 얼굴이면 name = 하위 폴더 이름
            names.append(name)
            
        # 인식한 얼굴 영역에 사각형과 이름을 출력
        for ((top, right, bottom, left), name) in zip(boxes, names):
            if name == "Unknown":
                color = (0, 0, 255)
                flag = -1
            else:
                color = (0, 255, 0)
                flag = 1
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if flag == 1: unlock()
        #if flag == 1: test()
        #if flag == 1: pass
        
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()
    
# 유저 정보를 삭제하는 메소드
def withdraw():
    pickle_dir = "/home/pi/Face_Recognition_Door_Lock/encoding/"
    # encoding 폴더가 없을 경우 종료
    if os.path.isdir(pickle_dir)==False:
        print("[Error] encoding folder is not exist")
        exit()
    
    while True:
        print("a. 특정 사용자 삭제, b. 모든 사용자 삭제, q. return")
        select = input("입력: ")
        
        if select == 'q':
            print("[Info] Return menu")
            break
            
        elif select == 'a':
            name = input("삭제할 이름 입력: ")
            if name == 'Unknown_Face':
                print("[Error] Can not deleted!")
                continue
            delete_name = name + ".pkl"
            delete_path = pickle_dir + delete_name
            
            # 파일이 없을 경우
            if os.path.isfile(delete_path) == False:
                print("[Error] file is not exist")
                continue
            
            print("삭제할 파일의 경로는 " + delete_path + " 입니다.")
            os.remove(delete_path)
            print("[Info] " + delete_name + " is deleted")
            
        elif select == 'b':
            for file in os.listdir(pickle_dir):
                if file.endswith(".pkl"):
                    if file == 'Unknown_Face.pkl': continue
                    os.remove(os.path.join(pickle_dir, file))
            print("[Info] Deleted all users")

if __name__ == '__main__':
    while True:
        print("a.register, b.recognition, c.withdraw, q.exit")
        x = input("select: ")
        if x == 'a':
            register()
        elif x == 'b':
            recognition()
        elif x == 'c':
            withdraw()
        elif x == 'q':
            exit()
        else:
            pass
        