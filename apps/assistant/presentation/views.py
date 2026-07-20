from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.assistant.domain.services import AssistantService
from apps.assistant.models import ChatMessage
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class AssistantView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "курсы"}
                },
                "required": ["message"]
            }
        },
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Ответ ассистента"),
            400: OpenApiResponse(description="Пустое сообщение"),
        },
        description="Виртуальный помощник: запрос курсов валют или конвертация",
    )

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