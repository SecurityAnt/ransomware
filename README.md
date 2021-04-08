# Python Thanos Ransomware Project

2019.2학기 경기대학교 컴퓨터보안 프로젝트

## preview
1. 메인화면
<img src="https://user-images.githubusercontent.com/48823900/114044833-8527fd80-98c2-11eb-80f6-74ddfcd97f76.png" width=500 height=300>
2. 최초에 암호화된 파일
<img src="https://user-images.githubusercontent.com/48823900/114044986-a4bf2600-98c2-11eb-809a-34a5824ccbcd.png" width=500 height=300>
3. 카운팅이 다 된 후 파일의 절반이 사라짐
<img src="https://user-images.githubusercontent.com/48823900/114045008-a852ad00-98c2-11eb-9ade-2b8e30134f2e.png" width=500 height=300>
4. 파일이 모두 삭제되었을때
<img src="https://user-images.githubusercontent.com/48823900/114045019-aab50700-98c2-11eb-9280-6b24e82ce76d.png" width=500 height=300>
5. 복호화키가 입력된 후
<img src="https://user-images.githubusercontent.com/48823900/114046189-9a515c00-98c3-11eb-911b-76e59c60baf5.png" width=500 height=300>

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
