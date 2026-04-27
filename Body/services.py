from abc import abstractmethod, ABC


class Body(ABC):

    @abstractmethod
    def get_head_keypoints(self,**kwargs):
        pass

    @abstractmethod
    def get_foot_keypoints(self,**kwargs):
        pass

    @abstractmethod
    def get_hands_keypoints(self,**kwargs):
        pass

    @abstractmethod
    def get_chest_keypoints(self, **kwargs):
        pass

    pass

class YoloBody(Body):

    def __init__(self, person, epp_required = None):
        self.person = person
        self._epp_required = {}


    def set_epp_required(self,**kwargs):
        self._epp_required = kwargs.get('epp_required')

        for pk, value in self._epp_required.items():
            self._epp_required[pk]["status"] = False

    def change_epp_status(self, **kwargs):

        epp_id = kwargs.get('epp_id')
        status = kwargs.get('status')

        self._epp_required[epp_id]["status"] = status

    def is_epp_complete(self):

        for pk, value in self._epp_required.items():
            if not self._epp_required[pk]["status"]:
                return False

        return True

    def return_missing_epp(self):

        missing_epp = []

        for pk, value in self._epp_required.items():
            if not self._epp_required[pk]["status"]:
                missing_epp.append(pk)

        return missing_epp

    def get_head_keypoints(self, **kwargs):
        return self.person[:5]

    def get_foot_keypoints(self, **kwargs):
        foot = [self.person[13], self.person[14], self.person[15], self.person[16]]
        return foot

    def get_hands_keypoints(self, **kwargs):
        hands = [self.person[7],self.person[8],self.person[9],self.person[10]]
        return hands

    def get_chest_keypoints(self, **kwargs):
        chest = [self.person[5], self.person[6], self.person[11], self.person[12]]
        return chest



