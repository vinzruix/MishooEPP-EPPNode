import time
from abc import ABC

import cv2
import requests
from jinja2.utils import missing

from Auth.exeptions import TokenExpired
from Multimedia.services import Multimedia


class Incidence:

    def __init__(self):
        self._incidences = 0
        self._epochs_clean = 0
        self._server_url = ""

    def increase_epochs(self):
        self._epochs_clean = 3

    def send_incidence_to_server(self, **kwargs):

        form_data = {
            "datetime": time.time(),
            "image": kwargs.get('image'),
            "missing_epp": kwargs.get('missing_epp')
        }

        response = requests.post(f"{self._server_url}", form_data)

        if response.ok:
            return

        if response.status_code == 401:
            raise TokenExpired()




    def set_url(self, **kwargs):
        self._server_url = kwargs.get('url')

    def incidence_handler(self, **kwargs):
        if self._incidences >= 3:
            self.send_incidence_to_server(**kwargs)
            self.reset_incidences()

        if self._epochs_clean >= 3:
            self.reset_incidences()

    def increase_incidences(self):
        self._incidences += 1

    def reset_incidences(self):
        self._incidences = 0
