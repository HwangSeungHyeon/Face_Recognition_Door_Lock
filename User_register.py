import cv2, os

print("사용자 이름을 입력하세요")
human_name = input()

# 폴더가 없다면 생성
save_path = "./data/people/"
img_path = save_path + human_name
if os.path.isdir(img_path) == False:
    os.mkdir(img_path)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 카메라로 비디오를 읽어옴
if not camera.isOpened():
    exit()
    
cnt = 0
while True:
    ret, frame = camera.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    cv2.imwrite(save_path + '/' + human_name + str(cnt) + ".jpg", frame)
    cnt += 1
    if cnt < 1:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
camera.release()
camera.destroyAllWindows()