import time
from abc import ABC

import cv2
import requests
from jinja2.utils import missing

from Auth.exeptions import TokenExpired
from Multimedia.services import Multimedia


class Incidence:

    def __init__(self, server_url):
        self._incidences = 0
        self._epochs_clean = 0
        self._server_url = server_url

    def increase_epochs(self):
        self._epochs_clean = 3

    def reset_epochs_clean(self):
        self._epochs_clean = 0

    def send_incidence_to_server(self, **kwargs):

        form_data = {
            "datetime": time.time(),
            "missing_epp": kwargs.get('missing_epp')
        }

        image_bytes = Multimedia.np_to_imageRGB_buffer(kwargs.get('image'), form_data["datetime"])


        try:
            response = requests.post(
                f"http://{self._server_url}/incidence/api/incidence/",
                data=form_data,
                files={
                    "image": ("photo.jpg", image_bytes, "image/jpeg")
                },
                headers={
                    "Authorization": f"Bearer {kwargs.get('access_token')}"
                }
            )

            if response.ok:
                return

            if response.status_code == 401 or response.status_code == 500:
                raise TokenExpired()


        except requests.exceptions.ConnectionError:
            raise ValueError("Server not found or down")

        except Exception as e:
            print(e)





    def set_url(self, **kwargs):
        self._server_url = kwargs.get('url')

    def incidence_handler(self, **kwargs):
        if self._incidences >= 3:
            self.send_incidence_to_server(**kwargs)
            self.reset_incidences()

        if self._epochs_clean >= 3:
            self.reset_incidences()
            self.reset_epochs_clean()

    def increase_incidences(self):
        print(self._incidences)
        self._incidences += 1

    def reset_incidences(self):
        self._incidences = 0
