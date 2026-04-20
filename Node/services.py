from Auth.services import AuthService
from Node.models import Node


class NodeFacade:
    def __init__(self, node: Node, auth:AuthService):
        self.node = node
        self.auth = auth

    def activate_node(self):
        self.node.is_active = True
        self.node.save()

    def deactivate_node(self):
        self.node.is_active = False
        self.node.save()

    def set_server_login_credentials(self,**kwargs):
        self.auth.set_credentials(username=kwargs.get('username'), password=kwargs.get("password"))

    def set_server_url(self,**kwargs):
        self.auth.set_url(url=kwargs.get('url'))

    def login_server(self):
        self.auth.authenticate()

    def send_node_data(self):
        self.node.refresh_from_db()

        if self.node.is_active:
            print("enviando algo xddxdxdxx")

        if not self.node.is_active:
            print("No haciendo nada xdxddx")