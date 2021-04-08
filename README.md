# Python Thanos Ransomware Project

2019.2학기 경기대학교 컴퓨터보안 프로젝트

## Contribute

박유지- [YujiPark]

김혜연- [hyeyeon0210]
ginahy0210@gmail.com

이미미- [@alal3960]
alal39603819@gmail.com  

박지우 - [@eraserrr]
a01074761054@gmail.com

## install
```
$ pip install -r requirements.txt
```
## 실행 파일 만들기
```
$ pyinstaller -F --uac-admin --key=[난독화를 위한 키] [프로젝트 위치]\ransomware\final.spec
```
## 디컴파일 하기
1. 디컴파일할 exe파일과 pyinstxtractor.py 한 폴더에 넣기(A폴더)
2. cmd 창에 A폴더 경로로 들어가 python pyinstxtractor.py [디컴파일할exe파일]
3. A폴더에서 새로 생성된 디컴파일링 결과 폴더에서 결과 확인
