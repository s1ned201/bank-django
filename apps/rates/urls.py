from django.urls import path
from .presentation.views import CurrentRatesView, RateHistoryView

app_name = 'rates'
urlpatterns = [
    path('', CurrentRatesView.as_view(), name='current_rates'),
    path('history/<str:currency_code>/', RateHistoryView.as_view(), name='rate_history'),
]