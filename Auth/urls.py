from django.urls import path

from Auth.views import CredentialsAPIView

urlpatterns = [
    path("api/credentials/epp_node/", CredentialsAPIView.as_view()),

]