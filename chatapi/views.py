from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatapi.serializers import ChatSerializer

from services.simple_rag_service import SimpleRagService

rag_service = SimpleRagService()

class ChatView(APIView):
    def _validate_message(self, message: str):
        """
        Validate the incoming message.
        
        Args:
            message: The message string to validate
            
        Raises:
            TypeError: If message is not a string
            ValueError: If message is empty, too short, or too long
        """
        # Type validation
        if not isinstance(message, str):
            raise TypeError("Message must be a string")
        
        # Empty/whitespace validation
        if not message or not message.strip():
            raise ValueError("Message cannot be empty or only whitespace")
        
        # Length validation
        if len(message) > 1500:
            raise ValueError("Message too long (maximum 1500 characters)")
        
        if len(message.strip()) < 3:
            raise ValueError("Message too short (minimum 3 characters)")
    
    def post(self, request):
        serializer = ChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data.get("message", "")
        
        # Validate the message
        try:
            self._validate_message(message)
        except (TypeError, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = rag_service.generate_answer(message)
            return Response({"response": response.get("answer", "No response")}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
