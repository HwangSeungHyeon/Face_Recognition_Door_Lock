from imutils.video import VideoStream
import face_recognition
import imutils, pickle, time
import cv2, numpy as np

cascade = "haarcascade_frontalface_default.xml"
encodings = "encoding/encodings.pkl"

data = pickle.loads(open(encodings, "rb").read())
detector = cv2.CascadeClassifier(cascade)

vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)


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
	
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	boxes = face_detection(frame)

	# 검출한 얼굴 영역의 embedding vector를 생성
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# 카메라로 촬영중인 사람의 얼굴과 pickle 파일에 저장된 embedding vector를 비교
	for encoding in encodings:
		matches = face_recognition.compare_faces(data["encodings"], encoding)
		name = "Unknown"

		face_distances = face_recognition.face_distance(data["encodings"], encoding)
		best_match_index = np.argmin(face_distances)
		if matches[best_match_index]:
    			name = data["names"][best_match_index]

		# 모르는 얼굴이면 name = "Unknown"
		# 아는 얼굴이면 name = 해당 폴더 이름
		names.append(name)

	# 인식한 얼굴 영역에 사각형과 이름을 출력
	for ((top, right, bottom, left), name) in zip(boxes, names):
		if(name == "Unknown"):
				color = (0, 0, 255)
		color = (0, 255, 0)
		cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()