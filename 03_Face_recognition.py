from imutils.video import VideoStream
import face_recognition
import imutils, pickle, time
import cv2, numpy as np
import pandas as pd, os

cascade = "haarcascade_frontalface_default.xml"

# encodings = "encoding/encodings.pkl"
# data = pickle.loads(open(encodings, "rb").read())

#--------------------------------------------------------#
# 2개의 pkl 데이터를 합치는 부분
base_dir = 'encoding/'
list1 = []
list2 = []

for fname in os.listdir(base_dir):
	temp = pd.read_pickle(os.path.join(base_dir, fname))
	for e in temp["encodings"]: list1.append(e)
	for n in temp["names"]: list2.append(n)

data = {"encodings": list1, "names": list2}
print("[INFO] Successfully read Pickle File!")
#--------------------------------------------------------#

detector = cv2.CascadeClassifier(cascade)

vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
# time.sleep(2.0)

def face_detection(frame):
    # 얼굴 검출에 사용할 gray 이미지와, 얼굴 인식에 사용할 rgb 이미지
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# 얼굴 영역을 검출
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

	# 검출한 얼굴 영역의 좌표가 들어있는 boxes
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	return boxes  

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width = 500)
	# flag = -1
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	boxes = face_detection(frame)
	# boxes = face_recognition.face_locations(rgb, model = "hog")

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
		if(name == "Unknown"):
    			# flag = -1
    			color = (0, 0, 255)
		else:
    			# flag = 1
    			color = (0, 255, 0)
		cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(50) & 0xFF

	if key == ord("q"):
		break

	# if(flag is 1):
    # 		time.sleep(1)
    # 		print("도어락 오픈")

cv2.destroyAllWindows()
vs.stop()