import os
import pickle
import numpy as np
import cv2
import mtcnn
from keras.models import load_model
from utils import get_face, l2_normalizer, normalize

# hyper-parameters
encoder_model = 'model/facenet_keras.h5'
people_dir = 'data/people'
encodings_path = 'encodings/encodings.pkl'
required_size = (160, 160)

face_detector = mtcnn.MTCNN()
face_encoder = load_model(encoder_model)

encoding_dict = dict()
encodes = []

# people 폴더 내에 있는 사진들을 불러옴
for img_name in os.listdir(people_dir):
    img_path = os.path.join(people_dir, img_name)

    # 이미지를 RGB 색상으로 읽음
    img = cv2.imread(img_path)
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 사진에서 얼굴을 감지 시도
    results = face_detector.detect_faces(img)
    # results = face_detector.detect_faces(img_rgb)

    # 사진에서 얼굴을 감지했다면
    if results:
        res = max(results, key = lambda b: b['box'][2] * b['box'][3])
        # face, _, _ = get_face(img_rgb, res['box'])
        face, _, _ = get_face(img, res['box'])
        face = normalize(face)
        face = cv2.resize(face, required_size)

        # 해당 얼굴을 모델에 넣어 도출한 결과 값을 encodes 리스트에 추가
        encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
        encodes.append(encode)

    if encodes:
        encode = np.sum(encodes, axis=0)
        encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
        encoding_dict[img_name] = encode


# 현재 등록된 인물 사진 리스트 출력
for key in encoding_dict.keys():
    print(key)

# 인물 리스트를 pickle 파일로 저장
with open(encodings_path, 'bw') as file:
    pickle.dump(encoding_dict, file)