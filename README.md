# Face_Recognition_Door_Lock
딥러닝을 기반으로 한 라즈베리파이 얼굴 인식 도어락을 만드는 프로젝트입니다.


## Development environment / 개발 환경
  * Raspberry pi 4 8gb / 라즈베리 파이 4 8gb
  * Raspberry Pi Touch Display / 라즈베리 파이 공식 7인치 터치 스크린
  * Raspberry pi 8MP Camera module v2 / 라즈베리파이 적외선 카메라 모듈 v2, 8MP
  * 5V 1-Chanel relay module POO109 / 1채널 5v 릴레이모듈 P00109
  * Mille Digital Doorlock MI-2300 / DC 밀레 디지털 도어락 MI-2300
  * Raspberry pi OS 32bit / 라즈베리파이 OS(구 라즈비안) 32비트
  * Thonny editor / 라즈비안 내장 토니 에디터

## Package / 필요 라이브러리
  * python 3.7.3
  * numpy 1.20.2
  * opencv 4.5.1 
  * imutils 0.5.4
  * pandas 1.2.4
  * face_recognition https://github.com/ageitgey/face_recognition/blob/master/README_Korean.md
  * picamera
  * time
  * os
  * GPIO
  * shutil
  * pickle

## Precondition / 사전 조건
  * Unknown Face 이미지 출처: All-Age-Faces-Dataset https://github.com/JingchunCheng/All-Age-Faces-Dataset/blob/master/README.md
  * 
  
## Download / 다운로드 방법
  * 주소를 깃허브 데스크탑에 붙여넣기 https://github.com/HwangSeungHyeon/Face_Recognition_Door_Lock.git
  * 또는 프로젝트를 원하는 폴더에 직접 다운로드

## Function / 기능
  * 사용자 사진 촬영 및 등록
  * 얼굴 인식을 이용한 잠금 해제
  * 특정 사용자 삭제
  * 모든 사용자 

## How to use / 사용 방법
  ## 1. 사용자 등록 with User_register.py and Train.py
       * User_resister.py 실행
       * 사람 이름을 입력받아 폴더 생성
       * 카메라 기능으로 해당 폴더에 이미지 저장
       * Train.py 실행
       * data/people 내부 폴더들의 이미지를 모두 불러옴
       * mtcnn을 이용해 사진에서 얼굴을 감지하면 해당 얼굴 영역을 모델에 학습
       * 폴더 이름으로 라벨링
   ![화면 캡처 2021-04-09 212930](https://user-images.githubusercontent.com/57141923/114180070-b49a4100-997a-11eb-8376-3aa197922dea.png)

  ## 2. 사용자 인식 with Video_recognition.py
  ![face_recognition](https://user-images.githubusercontent.com/57141923/114179575-21610b80-997a-11eb-9ff2-24f09d2bbef3.png)

 ## 3. 도어락 제어
    도어락 제어 영상: https://youtu.be/o0acUs2lJXM

## Built With / 개발에 참여한 사람
 * 황승현

## License / 라이센스
이 프로젝트는 MIT 라이센스로 라이센스가 부여되어 있습니다. 자세한 내용은 LICENSE.md 파일을 참고하세요.
