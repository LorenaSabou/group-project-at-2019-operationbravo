import base64
import json
import re
import time
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
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


def predict(net, labels, image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layer_outputs = net.forward(ln)
    end = time.time()

    print("[INFO] YOLO took {:.6f} seconds".format(end - start))
    return {'num_persons': get_num_person_predictions(layer_outputs, labels)}


def get_labels():
    labels = []
    with open('coco.names') as f:
        for line in f:
            labels.append(line.strip())
    return labels


def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return base64.b64decode(data, altchars)


def image_from_json(json_data):
    image_base64 = json_data['image']
    image_base64 = bytes(image_base64, encoding="ascii")
    image_data = Image.open(BytesIO(decode_base64(image_base64)))
    image_data.show()
    return image_data


app = Flask(__name__)

coco_labels = get_labels()
model = get_model()
image_server = 'http://192.168.3.2:1332'


def get_image_for_prediction():
    image_server_rest = image_server + '/rest/image'
    result = requests.get(image_server_rest)
    result = result.json()

    if 'image' in result:
        return image_from_json(result)

    return None


@app.route('/predict', methods=['GET', 'POST'])
def make_prediction():
    prediction_image = get_image_for_prediction()
    if prediction_image is not None:
        resp = json.dumps(predict(model, coco_labels, prediction_image))
    else:
        resp = json.dumps({'num_persons': 0})

    resp = Response(response=resp,
                    status=200,
                    mimetype="application/json")

    return resp


if __name__ == '__main__':
    http_server = WSGIServer(('', 1331), app)
    http_server.serve_forever()
