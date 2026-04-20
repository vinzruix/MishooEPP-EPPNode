from rest_framework import serializers

from Node.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['is_active','epp']



