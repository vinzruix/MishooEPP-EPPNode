import cv2
import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView

from MishooEPP_EPPNode.core.instances import  System
from Overlapper.services import YoloOverlapper


# Create your views here.

class EPPTestAPIView(APIView):

    def post(self,request):
        image = request.FILES['image']
        file_bytes = np.frombuffer(image.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        response = System.send_node_data(image=frame)
        return Response({"data":f"{response}"})
