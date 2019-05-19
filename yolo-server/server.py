import json
from typing import Tuple, List, Optional

from flask import Flask, Response
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import requests

from config.config import read_config
from ml.yolo import Yolo
from util.encoding import encode_image_base64
from util.image import image_from_json, draw_rectangles

app = Flask(__name__)
CORS(app)

server_config = read_config('config/server_config.json')
yolo_config = read_config('config/yolo_config.json')
model = Yolo(yolo_config['weights_path'], yolo_config['config_path'], yolo_config['labels_path'])


def get_room_image_for_prediction(room_address) -> Tuple[str, any]:
    """
    Returns the image to be used for the prediction from the raspberry pi server.
    :return: The image to be used for the prediction.
    """
    image_server_rest = room_address + server_config['image_rest_api']
    result = requests.get(image_server_rest)
    result = result.json()

    if 'image' in result:
        return result['room_name'], image_from_json(result)

    return result['room_name'], None


def find_room_address_by_id(r_id) -> Optional[str]:
    for room_id, room_address in server_config["rooms"].items():
        if room_id == r_id:
            return room_address
    return None


def get_prediction_from_image(image) -> List[Tuple[int, int, int, int]]:
    bounding_boxes = []
    if image is not None:
        bounding_boxes = model.predict(image)

    return bounding_boxes


@app.route('/predict', methods=['GET'])
def make_prediction() -> Response:
    """
    Return the number of persons prediction for all the available rooms.
    :return: the number of persons.
    """
    results = []
    for room_id, room_address in server_config["rooms"].items():
        room_name, prediction_image = get_room_image_for_prediction(room_address)
        bounding_boxes = get_prediction_from_image(prediction_image)
        predicted_image = encode_image_base64(draw_rectangles(prediction_image, bounding_boxes))
        results.append(
            {'num_persons': len(bounding_boxes), 'room_name': room_name, "id": room_id, "image": predicted_image}
        )

    resp = json.dumps({"rooms": results})
    resp = Response(response=resp,
                    status=200,
                    mimetype="application/json")

    return resp


@app.route('/predict_room/<room_id>', methods=['GET'])
def predict_for_room(room_id) -> Response:
    room_address = find_room_address_by_id(r_id=room_id)
    room_name, prediction_image = get_room_image_for_prediction(room_address=room_address)
    bounding_boxes = get_prediction_from_image(prediction_image)
    predicted_image = encode_image_base64(draw_rectangles(prediction_image, bounding_boxes))
    resp = {'num_persons': len(bounding_boxes), 'room_name': room_name, "id": room_id, "image": predicted_image}
    resp = json.dumps(resp)
    resp = Response(response=resp,
                    status=200,
                    mimetype="application/json")

    return resp


if __name__ == '__main__':
    print('Started server...')
    http_server = WSGIServer(('', 1331), app)
    http_server.serve_forever()
