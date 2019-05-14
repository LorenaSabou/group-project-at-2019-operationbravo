import base64
from io import StringIO, BytesIO

import cv2
from PIL import Image
import numpy as np


def read_image_base64(base64_string):
    image_base64 = bytes(base64_string, encoding="ascii")
    image_data = Image.open(BytesIO(image_base64))
    return cv2.cvtColor(np.array(image_data), cv2.COLOR_RGB2BGR)
