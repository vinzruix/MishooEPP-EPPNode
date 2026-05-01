from abc import ABC, abstractmethod


class Overlapper(ABC):

    def __init__(self, confidence=0.4):
        self._confidence = confidence

    @abstractmethod
    def is_inside(self, keypoints, equipment, body_part) -> bool:
        pass


class YoloOverlapper(Overlapper):

    def is_inside(self, keypoints, equipment, body_part="None") -> bool:
        for x, y, conf in keypoints:
            if conf > self._confidence:

                print(body_part)

                if body_part == "head":

                    if (equipment[0] <= int(x) <= equipment[2]) and ((int(y) >= equipment[1]) or (equipment[1] <= int(y) <= equipment[3])):
                        return True

                if not body_part == "head":
                    if (equipment[0] <= int(x) <= equipment[2]) and (equipment[1] <= int(y) <= equipment[3]):
                        return True
        return False
