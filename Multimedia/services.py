import io
import time

import cv2
from PIL import Image
from django.core.files.base import ContentFile
from picamera2 import Picamera2


class Multimedia:

    @staticmethod
    def take_photo_camera():
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            main={"size": (1280, 720)}
        )
        picam2.configure(config)

        picam2.start()

        frame = None

        for _ in range(10):
            frame = picam2.capture_array()
            time.sleep(0.05)

        picam2.stop()
        picam2.close()

        frame = frame[:, :, :3]


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
