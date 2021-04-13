from PIL import Image
from PIL import ImageOps
import os.path

#사진을 흑백으로 바꾼 후 히스토그램 평준화 처리하는 코드

targerdir = r"data/" #해당 폴더 설정 

files = os.listdir(targerdir)

format = [".jpg",".png",".jpeg","bmp",".JPG",".PNG","JPEG","BMP"] #지원하는 파일 형태의 확장자들
for (path,dirs,files) in os.walk(targerdir):
    for file in files:
         if file.endswith(tuple(format)):
             image = Image.open(path+"\\"+file).convert("L")
             image = ImageOps.equalize(image, mask = None)
             image.save(path+"\\"+file)

         else:
             print(path)
             print("InValid",file)