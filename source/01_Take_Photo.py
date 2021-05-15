from picamera import PiCamera, Color
import time, os

folder_dir = "dataset/Known/"

# 해당하는 폴더가 없을 경우 생성해줌
if os.path.isdir(folder_dir)==False:
    os.mkdir(folder_dir)

people_name = input("유저 이름: ")

save_path = folder_dir + people_name +"/"
print("저장할 폴더의 경로는 " + save_path + " 입니다.")

# 해당하는 폴더가 없을 경우 생성해줌
if os.path.isdir(save_path)==False:
    os.mkdir(save_path)
    
with PiCamera() as camera:
    camera.rotation = 90
    camera.annotate_text_size = 100
    camera.annotate_background = Color('red')
    camera.annotate_foreground = Color('yellow')
    
    camera.start_preview()
    camera.brightness = 50
    camera.exposure_mode = 'auto'
    
    for i in range(5, 0, -1):
        camera.annotate_text = str(i)
        time.sleep(1)
        
    camera.annotate_text = ""
    for i in range(10):
        time.sleep(0.5)
        camera.capture(save_path + people_name + '%s.jpg' %i)
            
    camera.annotate_text = "Finish!"
    time.sleep(2)
    camera.stop_preview()