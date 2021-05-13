# Face_Recognition_Door_Lock
딥러닝을 기반으로 한 라즈베리파이 얼굴 인식 도어락을 만드는 프로젝트입니다.

## 개발 환경
  * Raspberry pi 4 8gb / 라즈베리 파이 4 8gb
  * Raspberry Pi Touch Display / 라즈베리 파이 공식 7인치 터치 스크린
  * Raspberry pi 8MP Camera module v2 / 라즈베리파이 적외선 카메라 모듈 v2, 8MP
  * 5V 1-Chanel relay module POO109 / 1채널 5v 릴레이모듈 P00109
  * Mille Digital Doorlock MI-2300 / DC 밀레 디지털 도어락 MI-2300
  * Raspberry pi OS 32bit / 라즈베리파이 OS(구 라즈비안) 32비트
  * Thonny editor / 라즈비안 내장 토니 에디터

## 필요 라이브러리
  * python 3.7.3
  * numpy 1.20.2
  * opencv 4.5.1 
  * imutils 0.5.4
  * pandas 1.2.4
  * face_recognition
  * picamera
  * time
  * os
  * GPIO
  * shutil
  * pickle

## 사전 조건
  * 라즈베리 파이 OS 설치: https://blog.naver.com/ljy9378/221430062420
  * 라즈베리 파이 기본 설정: https://blog.naver.com/ljy9378/221430169621
  * 가상환경 사용법: https://sites.google.com/site/raspberrypieducation/programmingtools/python/pyvenv
  * opencv 설치 방법: https://webnautes.tistory.com/916
  * Unknown Face 이미지 출처: https://github.com/JingchunCheng/All-Age-Faces-Dataset/blob/master/README.md
  * GPIO 설치 방법: https://hoho325.tistory.com/212
  * 카메라 설정 및 picamera 라이브러리 설치: http://www.dreamy.pe.kr/zbxe/CodeClip/3769343
  * Face recognition 설치 방법: 콘솔창에 pip3 install face_recognition 입력
  
## 라즈베리 파이에 다운로드하는 방법
  1. open the terminal
  2. cd ~/원하는 위치
  3. git clone https://github.com/HwangSeungHyeon/Face_Recognition_Door_Lock.git

## Function / 기능
  * 사용자 사진 촬영 및 등록
  * 얼굴 인식을 이용한 잠금 해제
  * 특정 사용자 얼굴 삭제
  * 모든 사용자 얼굴 삭제

## How to use / 사용 방법
  ## 1. 사용자 등록
       1-1. Function.py 실행
       1-2. 사람 이름을 입력받으면 해당 이름을 가진 폴더가 생성
       1-3. 라즈베리 파이 카메라 모듈 v2로 사진을 촬영하기 전 5초의 유예 기간이 주어짐
       1-4. 0.5초의 간격으로 10장의 사진을 촬영
       1-5. 생성한 폴더에 사진을 저장
       1-6. 촬영한 사진에서 얼굴 영역 검출
       1-7a. 검출한 영역에 얼굴이 있을 경우 특징점 벡터를 추출
       1-7b. 검출한 영역에 얼굴이 없을 경우 PASS
       1-8a. 얼굴이 하나라도 존재할 경우 생성한 데이터로 "사용자 이름".pkl을 생성
       1-8b. 모든 사진에서 얼굴이 검출되지 않았을 경우 pkl 파일을 만들지 않고 종료
   ![seung_hyeon0](https://user-images.githubusercontent.com/57141923/118157873-0b050e80-b456-11eb-965f-315b911da261.jpg)

  ## 2. 사용자 인식
  ![face_recognition](https://user-images.githubusercontent.com/57141923/114179575-21610b80-997a-11eb-9ff2-24f09d2bbef3.png)

 ## 3. 도어락 제어
    도어락 제어 영상: https://youtu.be/o0acUs2lJXM

## Built With / 개발에 참여한 사람
 * 황승현

## License / 라이센스
이 프로젝트는 MIT 라이센스로 라이센스가 부여되어 있습니다. 자세한 내용은 LICENSE.md 파일을 참고하세요.
