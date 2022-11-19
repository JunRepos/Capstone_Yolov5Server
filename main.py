import io
import json
from flask import Flask, jsonify, request
from flask import make_response
import torchvision.transforms as transforms
import torch
from PIL import Image
import os
import pandas as pd
import base64
import json

app = Flask(__name__)
# yolo model 불러오기
model = torch.hub.load('yolov5-master', 'custom', path='yolov5-master/models/best.pt', source='local')
model.conf = 0.20  # NMS confidence threshold
model.iou = 0.20 # NMS IoU threshold
max_det = 1

category_class = {
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
print(category_class['203'])
print(11)
# POST 통신으로 들어오는 이미지를 저장하고 모델로 추론하는 과정
def save_image(file):
    file.save('./temp/' + file.filename)

@app.route('/', methods=['POST'])
def web():
    if request.method == 'POST':
        file = request.files['file']
        save_image(file)  # 들어오는 이미지 저장
        train_img = './temp/' + file.filename
        results = model(train_img)
        dectectFile = results.files
        print(dectectFile)
        detectImgPath = "C:/Users/JunPC/PycharmProjects/YoloFlask/runs/detect/exp/"

        results.save()
        print(type(results.pandas().xyxy[0]))
        print(results.pandas().xyxy[0])
        res_json = results.pandas().xyxy[0].to_json()
        # if not os.path.isfile(detectImgPath+dectectFile[0]):
        #     results_dict = {
        #         'img' : None
        #     }
        # else:
        with open(detectImgPath+dectectFile[0], "rb") as image_file:
            image_binary = image_file.read()
            encoded_string = base64.b64encode(image_binary)

            results_dict = {
                'img' : encoded_string.decode(),
            }

        img_json = json.dumps(results_dict)
        img_json_new = img_json[1:7] + '{"0":' + img_json[8:]
        print(img_json)

        results_json = res_json[0]+img_json_new+','+res_json[1:]
        results_json = json.loads(results_json)

        if(results_json['name']):
            print(results_json['name']['0'])
            results_json['name']['0'] = category_class[results_json['name']['0']]


        print(results_json)
        os.remove(train_img)

        return results_json

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090, debug=True)