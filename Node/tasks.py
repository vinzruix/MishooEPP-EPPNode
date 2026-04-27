from celery import shared_task
from MishooEPP_EPPNode.core.instances import System
from Multimedia.services import Multimedia


@shared_task
def send_data():
    System.send_node_data(image=Multimedia.take_photo_camera())