import io

import cv2
from PIL import Image
from django.core.files.base import ContentFile


class Multimedia:

    @staticmethod
    def take_photo_camera():
        capture = cv2.VideoCapture(0)
        frame = None

        for _ in range(10):
            ret, frame = capture.read()

        capture.release()

        return frame

    @staticmethod
    def cut_image(image, bounds):
        x1, y1, x2, y2 = map(int, bounds)
        return image[y1:y2, x1:x2]

    @staticmethod

    def np_to_imageRGB_buffer(np_array, filename):
        image = cv2.cvtColor(np_array, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        return ContentFile(buffer.read(), name=f"{filename}.jpg")
