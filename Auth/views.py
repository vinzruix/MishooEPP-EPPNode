from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from MishooEPP_EPPNode.core.instances import System




class CredentialsAPIView(APIView):

    @staticmethod
    def post(request):

        System.set_server_login_credentials(username=request.data['username'],password=request.data['password'])
        System.set_server_url(url=request.data['url'])
        System.login_server()
        System.activate_node()


        return Response({"success":"Credentials set"}, status=status.HTTP_200_OK)



