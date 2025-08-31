from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatapi.serializers import ChatSerializer


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data.get("message", "")
        
        response_message = f"Echo: {message}"
        return Response({"response": response_message}, status=status.HTTP_200_OK)
