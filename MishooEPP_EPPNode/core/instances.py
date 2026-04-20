from Auth.models import Credential, Token
from Auth.services import AuthService
from Node.models import Node
from Node.services import NodeFacade


node_object = Node.objects.first()
credential_object  = Credential.objects.first()
token_object = Token.objects.first()

if not node_object:
    node_object = Node.objects.create()

if not credential_object:
    credential_object = Credential.objects.create()

    token_object = Token.objects.get_or_create()


System = NodeFacade(node=node_object, auth=AuthService(credential=credential_object,token=token_object))