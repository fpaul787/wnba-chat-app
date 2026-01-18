from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatapi.serializers import ChatSerializer

from backend.services.simple_rag_service import SimpleRagService

rag_service = SimpleRagService()

class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data.get("message", "")
        
        try:
            response = rag_service.generate_answer(message)
            return Response({"response": response.get("answer", "No response")}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
