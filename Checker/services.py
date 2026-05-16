from abc import ABC, abstractmethod

from sympy import false
from ultralytics import YOLO
from Detector.services import Detector, YoloDetector
from Overlapper.services import Overlapper, YoloOverlapper
from Pose.exeptions import NoHumansDetected
from Pose.services import PoseLocator, YoloPoseLocator

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class Checker(ABC):

    @abstractmethod
    def check_epp_in_camera(self, **kwargs):
        pass

    @abstractmethod
    def set_epp_required(self, **kwargs):
        pass

    @abstractmethod
    def check_epp_correctly_used(self, **kwargs):
        pass

    pass


class YOLOChecker(Checker):
    def __init__(self, epp_detector: Detector = None, pose_locator: PoseLocator = None, overlapper: Overlapper = None):
        self.epp_detector = epp_detector or YoloDetector()
        self.pose_locator = pose_locator or YoloPoseLocator()
        self.overlapper = overlapper or YoloOverlapper()


    def check_epp_in_camera(self, **kwargs):
        return self.epp_detector.detect_epp_in_photo(**kwargs)

    def search_people_in_camera(self, **kwargs):
        return self.pose_locator.detect_human_in_photo(**kwargs)

    def check_epp_correctly_used(self, **kwargs):

        try:
            people = self.search_people_in_camera(**kwargs)
        except NoHumansDetected:
            return True


        for person in people:


            epp_detected = self.check_epp_in_camera(image=person[1])

            try:
                new_person = self.search_people_in_camera(image=person[1])
            except NoHumansDetected:
                continue


            is_user_using_epp_correctly, missing_epp = self.check_epp_overlap(epp=epp_detected, person=new_person[0][0])

            if not is_user_using_epp_correctly:
                return False, self.epp_detector.search_epp_name_by_id(epp_id=missing_epp), kwargs.get("image")


        return True, None, None

    def check_epp_overlap(self, **kwargs):
        epp = kwargs.get('epp')
        person = kwargs.get('person')
        person.set_epp_required(epp_required=self.epp_detector.epp_classes_id)

        for pk, value in epp.items():
            for equipment in value:
                keypoints_to_check = self.pose_locator.handle_person_epp(body_part=equipment["body_part"], person=person)
                if self.overlapper.is_inside(keypoints_to_check, equipment["bounds"], equipment["body_part"]):
                    person.change_epp_status(epp_id=pk,status=True)

        if person.is_epp_complete():
            return True, person.return_missing_epp()

        return False, person.return_missing_epp()


    def set_epp_required(self, **kwargs):
        logger.info(kwargs.get('epp_required'))
        self.epp_detector.handle_epp_classes(epp_required=kwargs.get('epp_required'))



