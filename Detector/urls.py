from django.urls import path
from Detector.views import EPPTestAPIView

urlpatterns = [
    path("", EPPTestAPIView.as_view()),

]