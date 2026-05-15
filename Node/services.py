import jwt

from Auth.exeptions import TokenExpired, CredentialsExpired
from Incidence.services import Incidence
from Auth.services import Authenticator
from Checker.services import Checker
from Node.models import Node


class NodeFacade:
    def __init__(self, node: Node, auth: Authenticator, checker: Checker, incidence: Incidence):
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

    def handle_permissions(self,**kwargs):
        return self.auth.handle_permission(**kwargs)


    def refresh_credentials(self):

        try:
            self.auth.refresh_token()
        except (CredentialsExpired, ValueError):
            self.deactivate_node()


    def login_server(self):
        self.auth.authenticate()

    def get_department_epp(self):
        token = self.auth.get_access_token()
        decoded = jwt.decode(token, options={"verify_signature": False})
        decoded = decoded["department"]["epp"]
        return decoded


    def get_access_token(self):
        return self.auth.get_access_token()



    def set_epp_required(self):
        self.checker.set_epp_required(epp_required=self.get_department_epp())

    def send_node_data(self, **kwargs):
        self.node.refresh_from_db()
        self.auth.credential.refresh_from_db()


        if not self.node.is_active:
            print("No haciendo nada xdxddx")
            return

        if self.node.is_active:
            self.set_epp_required()


            try:
                is_epp_used_correctly, missing_epp, image = self.checker.check_epp_correctly_used(**kwargs)
            except Exception as e:
                print(e)
                return

            if is_epp_used_correctly:
                self.incidence_handler.increase_epochs()

            if not is_epp_used_correctly:
                self.incidence_handler.increase_incidences()

            try:
                self.incidence_handler.set_url(self.auth.credential.url)
                self.incidence_handler.incidence_handler(missing_epp=missing_epp, image=image, access_token=self.get_access_token())
            except (TokenExpired, ValueError):
                self.refresh_credentials()
