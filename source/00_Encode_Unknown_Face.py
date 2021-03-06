# 02_Encode_Face.py와 유사한 코드입니다. 이걸로 먼저 Unknown 피클을 생성해주세요
from imutils import paths
import face_recognition
import pickle, os, cv2

# 이미지 경로에 한국어가 있으면 안 됩니다.
# 데이터 셋과 pickle 데이터를 저장할 경로 설정
datasets = "dataset/Unknown"
encodings_path = "encoding/Unknown_Face.pkl"

if os.path.isdir(datasets)==False:
    print("Unknown 폴더를 생성해주세요!")
    exit()
    # os.mkdir(datasets)

# 얼굴 탐지에는 hog 방식과 cnn 방식이 존재
# hog는 빠르지만 인식률이 떨어지고, cnn은 느리지만 인식률이 높음
model_name = "hog"

# datasets에 들어있는 폴더 출력
imagePaths = list(paths.list_images(datasets))

# 얼굴 embedding vector 데이터를 저장할 UnknownEncodings 리스트와, 이름을 저장할 UnknownNames 리스트
UnknownEncodings = []
UnknownNames = []

# 이미지 경로를 돌면서 얼굴의 embedding vector를 생성
for (i, imagePath) in enumerate(imagePaths):
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    name = "Unknown"

    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model = model_name)

    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        UnknownEncodings.append(encoding)
        UnknownNames.append(name)

# 이름과 embedding vector 데이터를, 설정한 경로에 pickle 파일로 저장
print("[INFO] serializing encodings...")
data = {"encodings": UnknownEncodings, "names": UnknownNames}

# 피클 파일 그냥 새로 만들기
with open(encodings_path, "wb") as f:
    f.write(pickle.dumps(data))
f.close()