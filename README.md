# 2022-2 Capstone 프로젝트 - 딥러닝 서버 파트
**메인 프로젝트 : 선박 부품 품질 관리 시스템 앱(inspected)**

Github 링크 : https://github.com/JunRepos/Capstone_AI

Yolov5 github : https://github.com/ultralytics/yolov5



|                |      						 |
|----------------|-------------------------------|
|**사용 언어**    |Python                        |
|**사용 프레임워크**|Flask, Pytorch              |
| **배포**        | AWS(Amazon Web Server)      | 

**요약**

>Yolov5를 이용해 객체 탐지하는 Flask 서버.  프론트엔드에서 이미지를 Post 받아 객체 탐지를 실행하고, 결과 이미지 및 내용을 json으로 저장 후 반환(이미지는 base64를 통하여 디코딩).

## 동작 방식

![img](https://user-images.githubusercontent.com/70323287/211944551-550438bb-5603-4613-9ddb-877884fdf354.png)

>이미지를 먼저 불량 검출 모델을 이용하여 불량 종류를 탐지한 후, 불량이 탐지 되지 않을 경우 부품 종류를 탐지한다(불량이 탐지될 경우 불량 유형으로 부품 판별 가능).

## 탐지 결과 반환 형식(json)

![image](https://user-images.githubusercontent.com/70323287/211945795-71b30d4d-e555-4012-ac9d-e116622b135b.png)
