from django.db import transaction
import jwt
from rest_framework.exceptions import NotAcceptable, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from scipy.linalg import rq

from MishooEPP_EPPNode.core.instances import System


class CredentialsAPIView(APIView):

    @staticmethod
    def post(request):


        try:
            with transaction.atomic():

                if not System.handle_permissions(request=request):
                    raise NotAuthenticated()

                System.set_server_login_credentials(username=request.data['id'], password=request.data['password'])
                System.set_server_url(url=request.data['server'])
                System.login_server()
                System.set_epp_required()
                System.activate_node()

        except Exception:
            raise NotAcceptable()

        return Response({"success": "Credentials set"}, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request):

        if not System.handle_permissions(request=request):
            raise NotAuthenticated()

        node_status = request.data["status"]

        if node_status is None:
            raise NotAcceptable()

        if node_status:
            System.activate_node()

        if not node_status:
            System.deactivate_node()

        return Response({"success": f"status changed to {node_status}"}, status=status.HTTP_200_OK)
