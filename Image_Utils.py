# 여기서는 사용하지 않습니다!!!!
# 폴더는 데이터 셋이 들어있는 최상단 폴더로 해주세요
# 예를 들어 dataset/p1, dataset/p2, dataset/p3 이런 식으로 구성이 되어 있다면
# targetdir = r"dataset" 

from PIL import Image
from PIL import ImageOps
import os.path

# 폴더 이름을 입력하면 이미지의 크기를 지정한 사이즈로 변경하는 메소드입니다.
def Size_Change(targetdir, width, height):
    files = os.listdir(targetdir)

    format = [".jpg",".png",".jpeg","bmp",".JPG",".PNG","JPEG","BMP"] #지원하는 파일 형태의 확장자들
    for (path,dirs,files) in os.walk(targetdir):
        for file in files:
            if file.endswith(tuple(format)):
                image = Image.open(path+"\\"+file)
                print(image.filename)
                print(image.size)

                image = image.resize((width, height), Image.LANCZOS)
                image.save(path+"\\"+file)
                print(image.size)

            else:
                print(path)
                print("InValid",file)

#폴더 이름을 입력하면 그레이스케일로 바꾼 후 히스토그램 평준화 처리하는 메소드입니다.
def Convert_Gray(targetdir):
    files = os.listdir(targetdir)

    format = [".jpg",".png",".jpeg","bmp",".JPG",".PNG","JPEG","BMP"] #지원하는 파일 형태의 확장자들
    for (path,dirs,files) in os.walk(targetdir):
        for file in files:
            if file.endswith(tuple(format)):
                image = Image.open(path+"\\"+file).convert("L")
                image = ImageOps.equalize(image, mask = None)
                image.save(path+"\\"+file)

            else:
                print(path)
                print("InValid",file)
    
