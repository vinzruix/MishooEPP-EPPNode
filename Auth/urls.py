from django.urls import path

from Auth.views import CredentialsAPIView

urlpatterns = [
    path("api/credentials/", CredentialsAPIView.as_view()),

]