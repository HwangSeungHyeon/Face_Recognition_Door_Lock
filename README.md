# Face_Recognition_Door_Lock
딥러닝을 기반으로 한 라즈베리파이 얼굴 인식 도어락을 만드는 프로젝트입니다.


## Package / 필요 패키지
  * Anaconda 4.9.2
  * python 3.7.9
  * tensorflow 2.4.1
  * keras 2.4.3
  * cuda 11.0
  * pickle 
  * numpy
  * mtcnn
  * opencv
  * Matplotlib
  * sklearn
  
## Download / 다운로드 방법
  * Download with Github desktop
    * 주소를 깃허브 데스크탑에 붙여넣기 (https://github.com/HwangSeungHyeon/Face_Recognition_Door_Lock.git)
  * Download project.Zip
    * 프로젝트를 원하는 폴더에 

## Function / 기능
  * 사용자 등록
  * 얼굴 탐지
  * 얼굴 분류
  * 잠금 해제 - 미구현

## How to use / 사용 방법
  * 사용자 등록 (User_register.py and Train.py)
      * User_resister.py 실행
      * 사람 이름을 입력받아 폴더 생성
      * 카메라 기능으로 해당 폴더에 이미지 저장
      * Train.py 실행
      * data/people 내부 폴더들의 이미지를 모두 불러옴
      * mtcnn을 이용해 사진에서 얼굴을 감지하면 해당 얼굴 영역을 모델에 학습
      * 폴더 이름으로 라벨링
  * 사용자 인식
 

## Built With / 개발에 참여한 사람
 * 황승현

## License / 라이센스
이 프로젝트는 MIT 라이센스로 라이센스가 부여되어 있습니다. 자세한 내용은 LICENSE.md 파일을 참고하세요.
