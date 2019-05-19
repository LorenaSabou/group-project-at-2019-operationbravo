import json
from typing import Tuple

from flask import Flask, Response
from gevent.pywsgi import WSGIServer
import requests

from config.config import read_config
from ml.yolo import Yolo
from util.image import image_from_json

app = Flask(__name__)

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


@app.route('/predict', methods=['GET', 'POST'])
def make_prediction() -> Response:
    """
    Return the number of persons prediction for all the available rooms.
    :return: the number of persons.
    """
    results = []
    for room_name, room_address in server_config["rooms"].items():
        room_name, prediction_image = get_room_image_for_prediction(room_address)

        num_persons = 0
        if prediction_image is not None:
            num_persons = model.predict(prediction_image)

        results.append({'num_persons': num_persons, 'room_name': room_name})

    resp = json.dumps({"rooms": results})
    resp = Response(response=resp,
                    status=200,
                    mimetype="application/json")

    return resp


if __name__ == '__main__':
    print('Started server...')
    http_server = WSGIServer(('', 1331), app)
    http_server.serve_forever()
