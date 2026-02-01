from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatapi.serializers import ChatSerializer

from services.rag_service import RagService

rag_service = RagService()

class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data.get("message", "")
        
        try:
            response = rag_service.generate_answer(message)
            return Response({"response": response.get("answer", "No response")}, status=status.HTTP_200_OK)
        except (TypeError, ValueError) as e:
            # Validation errors should return 400 Bad Request
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Other errors remain 500 Internal Server Error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
