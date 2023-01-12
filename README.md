# 2022-2 Capstone 프로젝트 - 딥러닝 서버 파트

## 개요
**세종대학교 2022-2 캡스톤 프로젝트 2조(inspected) 프로젝트 - 딥러닝 서버 파트**
|                |      				        |
|----------------|-------------------------------|
|**사용 언어**    |Python                         |
|**사용 메인 프레임워크**|Flask, Pytorch            |
| **배포**        | AWS(Amazon Web Server)        | 


### 요약

- Yolov5를 이용해 부품의 불량 여부 및 불량 종류, 부품 종류를 판별에 json 파일 형식으로 결과값을 반환해주는 Flask 서버.  
- 프론트엔드에서 이미지를 Post 받아 선박 부품의 불량 종류 및 부품 종류 객체 탐지를 실행하고, 결과 이미지 및 내용을 json으로 저장 후 반환(이미지는 base64를 통하여 디코딩).


## 서버
**서버 흐름도**

<img src="https://user-images.githubusercontent.com/70323287/211944551-550438bb-5603-4613-9ddb-877884fdf354.png" width="700" height="200"/>

- 전달 받은 이미지를 불량 검출 모델을 이용하여 불량 종류를 탐지한 후, 불량이 탐지 되지 않을 경우 부품 종류를 탐지한다(불량이 탐지될 경우 불량 유형으로 부품 판별 가능).


**탐지 결과 반환 형식 예시 (json)**

<img src=https://user-images.githubusercontent.com/70323287/211974604-b5f635b2-6b5b-4f52-98b7-1c46f79be1e2.png  width="700" height="500"/>


## 데이터셋

- 사용 데이터셋 : AI 허브의 부품 품질 검사 영상 데이터(선박·해양플랜트)
- 링크 : https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=579

**데이터셋 개요**

<img src="https://user-images.githubusercontent.com/70323287/211958272-e893fd53-ac2c-4f17-858d-b01decc817b8.png" width="700" height="700"/>

- 10가지 부품, 27가지 손상 종류를 포함한 데이터셋이 총 20만개 저장되어 있음.

### 불량 종류 탐지 데이터셋 

**불량 종류 탐지 데이터셋 개요**

<img src="https://user-images.githubusercontent.com/70323287/211961439-b6f780c0-3fbb-456b-8e41-a8448af9ed44.png" width="700" height="200"/>

- 전체 데이터셋에서 일부분 추출하여 학습 데이터셋 제작. (10개 부품 중 5개 부품 선별, 총 200,000개 데이터셋 중 54,371개 추출) 이미지 데이터의 용량을 감소 시키기 위하여 이미지 사이즈 축소
- FP(False Postive)의 감소를 위하여 정상품 이미지를 Background 이미지로 추가해 모델 개선 

**이미지 축소 예시**

<img src="https://user-images.githubusercontent.com/70323287/211972994-e82911e5-640a-421a-a093-f95c38087cae.png" width="700" height="200"/>

- 사진 한 개당 2.3mb에서 63kb로 축소 가능 

### 부품 종류 탐지 데이터셋 

- AI 허브에서는 부품 종류를 따로 바운딩박스 처리 하여 제공하지 않았기 때문에 Roboflow를 이용하여 직접 라벨링 처리

**RoboFlow 라벨링 처리 예시**

<img src="https://user-images.githubusercontent.com/70323287/211985089-9a4249be-41b8-497f-8967-67de18286071.png" width="700" height="400"/>

- 총 980개의 정상 이미지 데이터를 라벨링 처리 후 RoboFlow에서 제공하는 데이터 증강(Rotation, Flip) 을 통하여2,700개로 데이터 증강 

## Yolov5 학습 모델

**부품 불량 탐지 모델**

- 모델 종류 : Yolov5s(Pre-trained)
-  학습: Epochs : 300회
- 학습 툴 : Colab Pro

**모델 P-R Curve**

<img src="https://user-images.githubusercontent.com/70323287/211982964-1338327e-b291-4084-95bd-62f484a4f02c.png" width="700" height="400"/>


**부품 종류 탐지 모델**

- 모델 종류 : Yolov5m (Pre-trained)
-  학습: Epochs : 300회
- 학습 툴 : Colab Pro

**모델 P-R Curve**

<img src="https://user-images.githubusercontent.com/70323287/211983513-d86156b3-a68d-487c-847e-1a26143f28fb.png" width="700" height="400"/>

- 모델 둘 다 과대 적합 경향을 보여 lr0, lrf와 같은 하이퍼 파라미터 중 학습률(Learning rate)을 조정하는 방식을 통해 검증률 개선
