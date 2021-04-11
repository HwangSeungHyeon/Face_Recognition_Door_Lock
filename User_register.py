import cv2, random, string

save_path = "./data/people/"

# 숫자와 문자를 이용한 6자리의 이름 생성
char_set = string.ascii_lowercase + string.digits
userId = ''.join(random.sample(char_set*6, 6))

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 카메라로 비디오를 읽어옴
if not camera.isOpened():
    exit()

flag = 0
while True:
    ret, frame = camera.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    # 사진을 딱 1장만 찍음
    if flag == 1:
        cv2.imwrite(save_path + '/' + userId + ".jpg", frame)
        flag = 0
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
camera.release()
camera.destroyAllWindows()