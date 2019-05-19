from typing import List, Tuple

import cv2
import numpy as np

from PIL import Image

from ml.model import get_model


class Yolo(object):
    def __init__(self, weights_path: str, config_path: str, labels_path: str, **kwargs):
        self._model = self._initialize(weights_path, config_path)
        self._labels = self._get_labels(labels_path)

        self._IMAGE_WIDTH = 1024
        self._IMAGE_HEIGHT = 768
        self._PERSON_LABEL = 'person'
        self.SIZE = (self._IMAGE_WIDTH, self._IMAGE_HEIGHT)

        self.confidence_threshold = 0.6

        if 'confidence_threshold' in kwargs:
            self.confidence_threshold = kwargs['confidence_threshold']

    @staticmethod
    def _initialize(weights_path: str, config_path: str):
        """
        Initializes the yolo model with the provided weights and config.
        :param weights_path: The nn weights.
        :param config_path: The yolo arhitecture config.
        :return: the yolo model.
        """
        return get_model(weights_path, config_path)

    @staticmethod
    def _get_labels(labels_path: str)-> List[str]:
        """
        Reads the labels associated with the yolo NN.
        :param labels_path: the path for the labels.
        :return: the labels list.
        """
        labels = []
        with open(labels_path) as f:
            for line in f:
                labels.append(line.strip())
        return labels

    def _get_label_from_detection(self, detection: List[any]) -> Tuple[str, float]:
        """
        Returns the label and confidence from the output layer detection.
        :param detection: The output layer detection.
        :return: the label and confidence for a detection.
        """
        scores = detection[5:]
        label_id = np.argmax(scores)
        label = self._labels[label_id]
        confidence = scores[label_id]
        return label, confidence

    def _is_person_detection(self, detection) -> bool:
        """
        Checks if a given detection contains a person.
        :param detection: the output layer detection.
        :return: wether a detection is for a person or not.
        """
        label, confidence = self._get_label_from_detection(detection=detection)
        if confidence >= self.confidence_threshold and label == self._PERSON_LABEL:
            return True

        return False

    def _get_bounding_box_from_detection(self, detection) -> Tuple[int, int, int, int]:
        # scale bounding box relative to the image size
        center_x = int(detection[0] * self._IMAGE_WIDTH)
        center_y = int(detection[1] * self._IMAGE_HEIGHT)
        w = int(detection[2] * self._IMAGE_WIDTH)
        h = int(detection[3] * self._IMAGE_HEIGHT)

        # the coordinates are returned relative to the center of the object
        # so we must compensate for that
        x = int(center_x - (w / 2))
        y = int(center_y - (h / 2))

        return x, y, int(w), int(h)

    def _get_person_bounding_boxes(self, layer_outputs) -> List[Tuple[int, int, int, int]]:
        """
        Returns the number of persons from the layer outputs.
        :param layer_outputs: the output layer predictions.
        :return: the number of persons.
        """
        bounding_boxes = []
        for output in layer_outputs:
            person_detections = [detection for detection in output if self._is_person_detection(detection)]
            current_bounding_boxes = [self._get_bounding_box_from_detection(d) for d in person_detections]
            bounding_boxes.extend(current_bounding_boxes)

        return bounding_boxes

    def _get_output_layers(self):
        layer_names = self._model.getLayerNames()
        layer_names = [layer_names[i[0] - 1] for i in self._model.getUnconnectedOutLayers()]
        return layer_names

    def predict(self, image: Image) -> List[Tuple[int, int, int, int]]:
        """
        Predict bounding boxes for the persons in the image.
        :param image: the PIL image
        :return: the bounding boxes for the persons in the image.
        """
        # convert the PIL image to a CV image
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        layer_names = self._get_output_layers()

        size = (self._IMAGE_WIDTH, self._IMAGE_HEIGHT)
        image = cv2.resize(image, size)
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, swapRB=True, crop=False)

        # set the input for the yolo model
        self._model.setInput(blob)

        # get the predictions from the model
        layer_outputs = self._model.forward(layer_names)

        # the output is the number of persons found in the picture
        return self._get_person_bounding_boxes(layer_outputs)

