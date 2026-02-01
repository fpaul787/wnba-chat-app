from rest_framework import serializers

from chatapi.models import ChatMessage

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message', 'timestamp']