import json
import time

import cv2
import numpy as np
from flask import Flask, Response
from gevent.pywsgi import WSGIServer
import requests


def get_model():
    weights_path = "yolov3-spp.weights"
    config_path = "yolov3-spp.cfg"

    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    return net


def get_num_person_predictions(layer_outputs, labels, confidence_threshold=0.6):
    num_persons = 0

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            label = labels[classID]
            confidence = scores[classID]
            if confidence >= confidence_threshold and label == 'person':
                num_persons += 1

    return num_persons


def predict(net, labels, image_path):
    image = cv2.imread(image_path)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layer_outputs = net.forward(ln)
    end = time.time()

    print("[INFO] YOLO took {:.6f} seconds".format(end - start))
    return get_num_person_predictions(layer_outputs, labels)


def get_labels():
    labels = []
    with open('coco.names') as f:
        for line in f:
            labels.append(line.strip())
    return labels


app = Flask(__name__)

coco_labels = get_labels()
model = get_model()
image_server = 'http://192.168.3.2:1332'


def get_image_for_prediction():
    image_server_rest = image_server + '/rest/image'
    result = requests.get(image_server_rest)
    print(result.json())
    return 'example4.jpg'


@app.route('/predict', methods=['GET', 'POST'])
def make_prediction():
    prediction_image = get_image_for_prediction()
    resp = json.dumps(predict(model, coco_labels, prediction_image))
    resp = Response(response=resp,
                    status=200,
                    mimetype="application/json")

    return resp


if __name__ == '__main__':
    http_server = WSGIServer(('', 1331), app)
    http_server.serve_forever()
