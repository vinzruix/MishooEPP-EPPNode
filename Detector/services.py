from abc import ABC, abstractmethod
from ultralytics import YOLO


class Detector(ABC):

    @abstractmethod
    def detect_epp_in_photo(self, **kwargs):
        pass


class YoloDetector(Detector):

    def __init__(self, model : YOLO =None, epp_classes= None, confidence = 0.5):
        self.epp_classes = epp_classes
        self.epp_classes_id = {}
        self.model = model or YOLO("Detector/best.pt")
        self.confidence = confidence

    def detect_epp_in_photo(self,**kwargs):
        results = self.model(kwargs.get('image'))
        epp = {}


        for result in results:
            for box in result.boxes:
                if int(box.cls.item()) in self.epp_classes_id:
                    if box.conf > self.confidence:

                        epp.setdefault(box.cls.item(),[]).append({
                            "bounds" : box.xyxy[0],
                            "body_part" : self.epp_classes_id[int(box.cls.item())]["body_part"]
                        })

        return epp


    def handle_epp_classes(self,**kwargs):
        self.epp_classes = kwargs.get('epp_required')

        for pk,name in self.model.names.items():
            if name in self.epp_classes:
                self.epp_classes_id[pk] = self.epp_classes[name]

    def search_epp_name_by_id(self, **kwargs):
        epp_id = kwargs.get("epp_id")
        names = []

        for pk in epp_id:
            if pk in self.model.names:
                names.append(self.model.names[pk])

        return names

















