from celery import shared_task
from MishooEPP_EPPNode.core.instances import System



@shared_task
def send_data():
    System.send_node_data()