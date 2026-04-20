import requests

from Auth.models import Credential, Token


def send_data_to_server():
    credentials = Credential.objects.first()

    response = requests.get(f"{credentials.url}/users/api/users/",headers={
        "Authorization" : f"Bearer {credentials.tokens.access}",
    })

    if not response.ok:
        pass



