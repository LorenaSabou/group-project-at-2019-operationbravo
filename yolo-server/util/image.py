from io import BytesIO
from typing import Dict

from PIL import Image

from util.encoding import decode_base64


def image_from_json(json_data: Dict[str, str]) -> Image:
    image_base64 = json_data['image']
    image_base64 = bytes(image_base64, encoding="ascii")
    image_data = Image.open(BytesIO(decode_base64(image_base64)))
    image_data.show()
    return image_data
