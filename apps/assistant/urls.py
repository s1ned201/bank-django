from django.urls import path
from .presentation.views import AssistantView

app_name = 'assistant'

urlpatterns = [
    path('', AssistantView.as_view(), name='ask'),
]