from Auth.exeptions import TokenExpired, CredentialsExpired
from Incidence.services import Incidence
from Multimedia.services import Multimedia
from Auth.services import AuthService, Authenticator
from Checker.services import Checker
from Node.models import Node


class NodeFacade:
    def __init__(self, node: Node, auth: Authenticator, checker: Checker, incidence: Incidence = Incidence()):
        self.node = node
        self.auth = auth
        self.checker = checker
        self.incidence_handler = incidence

    def activate_node(self):
        self.node.is_active = True
        self.node.save()

    def deactivate_node(self):
        self.node.is_active = False
        self.node.save()

    def set_server_login_credentials(self, **kwargs):
        self.auth.set_credentials(username=kwargs.get('username'), password=kwargs.get("password"))

    def set_server_url(self, **kwargs):
        self.auth.set_url(url=kwargs.get('url'))
        self.incidence_handler.set_url(url=kwargs.get('url'))

    def refresh_credentials(self):

        try:
            self.auth.refresh_token()
        except CredentialsExpired:
            self.deactivate_node()


    def login_server(self):
        self.auth.authenticate()

    def set_epp_required(self, **kwargs):
        self.checker.set_epp_required(epp_required=kwargs.get("epp_required"))

    def send_node_data(self, **kwargs):
        self.node.refresh_from_db()

        # if self.node.is_active:

        is_epp_used_correctly, missing_epp, image = self.checker.check_epp_correctly_used(**kwargs)

        if is_epp_used_correctly:
            self.incidence_handler.increase_epochs()

        if not is_epp_used_correctly:
            self.incidence_handler.increase_incidences()

        try:
            self.incidence_handler.incidence_handler(missing_epp=missing_epp, image=image)
        except TokenExpired:
            self.refresh_credentials()

        # if not self.node.is_active:
        #  print("No haciendo nada xdxddx")
