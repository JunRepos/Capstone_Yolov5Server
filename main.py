from flask import Flask, request
import torch
import os
import base64
import json

app = Flask(__name__)
# yolo model 불러오기
model_damage = torch.hub.load('yolov5-master', 'custom', path='yolov5-master/models/DamageDetect.pt', source='local')
model_part = torch.hub.load('yolov5-master', 'custom', path='yolov5-master/models/PartDetect.pt', source='local')

model_damage.conf = 0.2  # NMS confidence threshold
model_damage.iou = 0.2 # NMS IoU threshold
model_damage.max_det = 1

model_part.conf = 0.2  # NMS confidence threshold
model_part.iou = 0.2 # NMS IoU threshold
model_part.max_det = 1

category_class_damage = {
    '203': '덕트손상', # 덕트 손상 (덕트)
    '209': '연결불량', # 연결 불량 (덕트)
    '212': '테이프불량', # 테이프 불량 (덕트)
    '401': '볼트체결불량', # 볼트 체결 불량 (선박 배관)
    '402': '파이프손상', # 파이프 손상 (선박 배관)
    '202': '단차', # 단차 (선체)
    '206': '보강재설치불량', # 보강재 설치 불량 (선체)
    '205': '바인딩불량', # 바인딩 불량 (케이블)
    '208': '설치불량', # 설치 불량 (케이블)
    '211': '케이블손상', # 케이블 손상 (케이블)
    '201': '가공불량', # 가공 불량 (보온재)
    '207': '보온재손상', # 보온재 손상 (보온재)
    '210': '연계처리불량', # 연계 처리 불량 (보온재)
    '213': '함석처리불량' # 함석 처리 불량 (보온재)
}

category_class_part = {
    '203': '덕트', # 덕트 손상 (덕트)
    '209': '덕트', # 연결 불량 (덕트)
    '212': '덕트', # 테이프 불량 (덕트)
    '401': '선박배관', # 볼트 체결 불량 (선박 배관)
    '402': '선박배관', # 파이프 손상 (선박 배관)
    '202': '선체', # 단차 (선체)
    '206': '선체', # 보강재 설치 불량 (선체)
    '205': '케이블', # 바인딩 불량 (케이블)
    '208': '케이블', # 설치 불량 (케이블)
    '211': '케이블', # 케이블 손상 (케이블)
    '201': '보온재', # 가공 불량 (보온재)
    '207': '보온재', # 보온재 손상 (보온재)
    '210': '보온재', # 연계 처리 불량 (보온재)
    '213': '보온재' # 함석 처리 불량 (보온재)
}



# POST 통신으로 들어오는 이미지를 저장하고 모델로 추론하는 과정
def save_image(file):
    file.save('./temp/' + file.filename)

@app.route('/', methods=['POST'])
def web():
    if request.method == 'POST':
        file = request.files['file']
        save_image(file)  # Post 받은 이미지 저장
        train_img = './temp/' + file.filename # 받은 이미지 경로

        results_dict = { # return할 결과값 지정
            "type": "",
            'img': "",
            'part': "",
            'name': "",
            'xmin': "",
            'ymin': "",
            'xmax': "",
            'ymax': "",
            'confidence': "",
        }

        results = model_damage(train_img)

        dectectFile = results.files

        detectImgPath = "C:/Users/JunPC/PycharmProjects/YoloFlask/runs/detect/exp/"
        detectImg = detectImgPath + dectectFile[0]
        results.save()
        res_json = results.pandas().xyxy[0].to_json()
        res_damage_json = json.loads(res_json)

        if (res_damage_json['name']): # 불량으로 분류가 됬다면
            with open(detectImg, "rb") as image_file:

                #Base64를 통하여 이미지 디코딩
                image_binary = image_file.read()
                encoded_string = base64.b64encode(image_binary)

                #결과값 저장
                results_dict['type'] = "불량품"
                results_dict['img'] = encoded_string.decode()
                results_dict['part'] = category_class_part[res_damage_json['name']['0']]
                results_dict['name'] = category_class_damage[res_damage_json['name']['0']]
                results_dict['xmin'] = res_damage_json['xmin']['0']
                results_dict['ymin'] = res_damage_json['ymin']['0']
                results_dict['xmax'] = res_damage_json['xmax']['0']
                results_dict['ymax'] = res_damage_json['ymax']['0']
                results_dict['confidence'] = res_damage_json['confidence']['0']

                image_file.close()
                os.remove(detectImg)

        else: # 불량으로 검출이 안됬다면(정상)
            os.remove(detectImg)
            results_part = model_part(train_img) # 부품 분류 모델로 한번 더 detect
            dectectFile = results_part.files
            detectImg = detectImgPath + dectectFile[0]
            results_part.save()

            res_json = results_part.pandas().xyxy[0].to_json()
            res_part_json = json.loads(res_json)

            if(res_part_json['name']): #분류가 됬다면 (부품 분류)
                with open(detectImg, "rb") as image_file:
                    image_binary = image_file.read()
                    encoded_string = base64.b64encode(image_binary)

                    results_dict['type'] = "정상품"
                    results_dict['img'] = encoded_string.decode()
                    results_dict['part'] = category_class_part[res_part_json['name']['0']]
                    results_dict['name'] = "정상"
                    results_dict['xmin'] = res_part_json['xmin']['0']
                    results_dict['ymin'] = res_part_json['ymin']['0']
                    results_dict['xmax'] = res_part_json['xmax']['0']
                    results_dict['ymax'] = res_part_json['ymax']['0']
                    results_dict['confidence'] = res_part_json['confidence']['0']

                    image_file.close()
                    os.remove(detectImg)

            else:
                os.remove(detectImg)
                with open(train_img, "rb") as image_file:
                    image_binary = image_file.read()
                    encoded_string = base64.b64encode(image_binary)

                    results_dict['type'] = "정상품"
                    results_dict['img'] = encoded_string.decode()
                    results_dict['name'] = "검출 실패"
                    results_dict['part'] = "검출 실패"
                    results_dict['xmin'] = 0.0
                    results_dict['ymin'] = 0.0
                    results_dict['xmax'] = 0.0
                    results_dict['ymax'] = 0.0
                    results_dict['confidence'] = 0.0

                    image_file.close()

        os.remove(train_img)
        return results_dict

if __name__ == "__main__":
    app.run(host="43.201.111.34", port="5000")