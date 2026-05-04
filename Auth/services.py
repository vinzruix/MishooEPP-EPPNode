from abc import ABC, abstractmethod

import jwt
import requests
from rest_framework.exceptions import NotAuthenticated

from Auth.exeptions import CredentialsExpired
from Auth.models import Credential, Token


class Authenticator(ABC):
    @abstractmethod
    def set_credentials(self,**kwargs):
        pass

    @abstractmethod
    def set_url(self,**kwargs):
        pass

    @abstractmethod
    def authenticate(self, **kwargs):
        pass

    @abstractmethod
    def handle_permission(self, **kwargs):
        pass


    @abstractmethod
    def get_access_token(self, **kwargs):
        pass

    @abstractmethod
    def refresh_token(self, **kwargs):
        pass


class AuthService(Authenticator):
    def __init__(self, credential:Credential, token:Token):
        self.token = token
        self.credential = credential


    def set_credentials(self,**kwargs):
        self.credential.username = kwargs.get('username')
        self.credential.password = kwargs.get('password')
        self.credential.save()

    def set_url(self,**kwargs):
        self.credential.url = kwargs.get('url')
        self.credential.save()

    def handle_permission(self,**kwargs):

        try:
            header = kwargs.get("request").META.get('HTTP_AUTHORIZATION', '')
            token = header.split(' ')[-1]
            permissions = jwt.decode(token, options={"verify_signature": False})


            if "sensors.create_sensor" in permissions["permissions"]:
                return True

        except Exception as e:
            print(e)
            pass


        return False



    def authenticate(self):
        self.credential.refresh_from_db()
        self.token.refresh_from_db()


        try:
            response = requests.post(f"http://{self.credential.url}/epp_detection/api/epp_detection/node/token/",
                                     json={
                                         "username": self.credential.username,
                                         "password": self.credential.password
                                     })

            if response.ok:
                response = response.json()
                self.set_tokens(access=response['access'],refresh=response["refresh"])
                return

            if response.status_code == 401:
                self.set_credentials(username='', password='')

            raise CredentialsExpired("Credentials not working")

        except requests.exceptions.ConnectionError:
            raise ValueError("Server not found or down")


    def set_tokens(self,**kwargs):
        self.token.refresh = kwargs.get("refresh")
        self.token.access = kwargs.get("access")
        self.token.save()

    def get_access_token(self):
        self.token.refresh_from_db()
        return self.token.access




    def refresh_token(self):
        self.token.refresh_from_db()
        self.credential.refresh_from_db()

        try:
            response = requests.post(f"http://{self.credential.url}/epp_detection/api/epp_detection/node/token/refresh/",
                                     json={
                                         "refresh": self.token.refresh,
                                     })

            if response.ok:
                response = response.json()
                self.set_tokens(refresh=self.token.refresh, access=response['access'])

            if response.status_code == 401:
                self.set_tokens(refresh="", access="")
                self.authenticate()


        except requests.exceptions.ConnectionError:
            raise ValueError("Server not found or down")


