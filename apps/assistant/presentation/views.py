from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.assistant.domain.services import AssistantService
from apps.assistant.models import ChatMessage

class AssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message', '').strip()
        if not message:
            return Response({'error': 'Сообщение не может быть пустым'}, status=400)

        service = AssistantService()
        response_text = service.process_message(request.user, message)

        ChatMessage.objects.create(
            user=request.user,
            message=message,
            response=response_text
        )

        return Response({'response': response_text})