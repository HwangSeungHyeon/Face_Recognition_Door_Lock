from imutils.video import VideoStream
import face_recognition
import imutils, pickle, time
import cv2, numpy as np
import pandas as pd, os
import Doorlock_Control
from utils import Rotate
from picamera import PiCamera

# 2개의 pkl 데이터를 합치는 부분
base_dir = 'encoding/'
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
    
    boxes = face_recognition.face_locations(gray, model = "hog")

    # 검출한 얼굴 영역의 embedding vector를 생성
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # 카메라로 촬영중인 사람의 얼굴과 pickle 파일에 저장된 embedding vector를 비교
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance = 0.6)
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
    #if flag == 1: Doorlock_Control.test()

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()