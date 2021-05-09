#01_Take_Photo.py 파일로 만든 얼굴 사진을 인코딩하는 단계입니다.
from imutils import paths
import face_recognition
import pickle, os, cv2

#이미지 경로에 한국어가 있으면 안 됩니다.
#데이터 셋과 pickle 데이터를 저장할 경로 설정
datasets = "dataset/Known"
encodings_path = "encoding/Known_Face.pkl"

#얼굴 탐지에는 hog 방식과 cnn 방식이 존재
#hog는 빠르지만 인식률이 떨어지고, cnn은 느리지만 인식률이 높음
model_method = 'hog'

#datasets에 들어있는 이미지 list
imagePaths = list(paths.list_images(datasets))

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
    boxes = face_recognition.face_locations(rgb, model = model_method)
    
    # 박스 영역의 얼굴 임베딩 데이터를 추출
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    # loop over the encodings
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

# 얼굴 임베딩 데이터와 이름을 pickle 파일로 저장
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}

with open(encodings_path, "wb") as f:
    f.write(pickle.dumps(data))
f.close()