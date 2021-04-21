from imutils import paths
import face_recognition
import pickle, os, cv2

# 이미지 경로에 한국어가 있으면 안 됩니다.
# 데이터 셋과 pickle 데이터를 저장할 경로 설정
datasets = "dataset"
encodings_path = "encoding/encodings.pkl"

# 얼굴 탐지에는 hog 방식과 cnn 방식이 존재
# hog는 빠르지만 인식률이 떨어지고, cnn은 느리지만 인식률이 높음
model_name = "hog"

# datasets에 들어있는 폴더 출력
imagePaths = list(paths.list_images(datasets))

# 얼굴 embedding vector 데이터를 저장할 knownEncodings 리스트와, 학습한 얼굴 이름을 저장할 knownNames 리스트
knownEncodings = []
knownNames = []

# 이미지 경로를 돌면서 얼굴을 학습
for (i, imagePath) in enumerate(imagePaths):
	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	boxes = face_recognition.face_locations(rgb, model = model_name)

	encodings = face_recognition.face_encodings(rgb, boxes)

	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)

# 이름과 embedding vector 데이터를 설정한 경로에 pickle 파일로 저장
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}

# 피클 파일 그냥 새로 만들기
f = open(encodings_path, "wb")
f.write(pickle.dumps(data))
f.close()