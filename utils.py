import cv2, pickle, numpy as np
from sklearn.preprocessing import Normalizer

# get encode
def get_encode(face_encoder, face, size):
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
    return encode

# 얼굴 영역 잘라내기
def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)

# 유클리드 거리가 1이 되도록 데이터를 조정
l2_normalizer = Normalizer('l2')

# 정규화
def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std

# pickle 파일 가져오기
def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict