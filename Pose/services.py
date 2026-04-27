import io
from abc import ABC, abstractmethod

import cv2
from ultralytics import YOLO

from Body.services import Body, YoloBody
from Multimedia.services import Multimedia
from Pose.exeptions import NoHumansDetected


class PoseLocator(ABC):
    @abstractmethod
    def detect_human_in_photo(self, image):
        pass


class YoloPoseLocator(PoseLocator):

    def __init__(self, model: YOLO = None, body_handler: Body = None, confidence=0.8, epp_required=None):
        self.model = model or YOLO("Pose/yolov8n-pose.pt")
        self.body_handler = body_handler or YoloBody
        self.confidence = confidence

    def detect_human_in_photo(self, **kwargs):

        results = self.model(kwargs.get('image'), verbose=False)
        persons = []

        for result in results:
            for box, keypoints in zip(result.boxes, result.keypoints.data):
                if box.conf > self.confidence:
                    persons.append([
                        self.body_handler(keypoints),
                        Multimedia.cut_image(image=kwargs.get('image'), bounds=box.xyxy[0])
                    ])

        if len(persons) == 0:
            raise NoHumansDetected

        return persons

    @staticmethod
    def handle_person_epp(**kwargs):
        body_part = kwargs.get('body_part')
        person = kwargs.get("person")

        if body_part == "head":
            return person.get_head_keypoints()

        if body_part == "foot":
            return person.get_foot_keypoints()

        if body_part == "hands":
            return person.get_hands_keypoints()

        if body_part == "chest":
            return person.get_chest_keypoints()

        return None
