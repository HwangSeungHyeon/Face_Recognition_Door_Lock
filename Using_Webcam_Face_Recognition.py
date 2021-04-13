from scipy.spatial.distance import cosine
from keras.models import load_model
from utils import *
import mtcnn

def recognize(img, detector, encoder, encoding_dict, recognition_t=0.4, confidence_t=0.99, required_size=(160, 160), ):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = 'unknown'

        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)

            # 이미 학습된 얼굴일 경우 name을 unknown에서 변경
            if dist < recognition_t and dist < distance:
                name = "known"
                distance = dist

        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, "Denied", pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, "Grandted", (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 200), 2)
    return img

encoder_model = 'model/facenet_keras.h5'
encodings_path = 'encodings/encodings.pkl'

face_detector = mtcnn.MTCNN()
face_encoder = load_model(encoder_model)
encoding_dict = load_pickle(encodings_path)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("카메라를 열 수 없습니다.")
        break
    frame = recognize(frame, face_detector, face_encoder, encoding_dict)
    cv2.imshow('camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break