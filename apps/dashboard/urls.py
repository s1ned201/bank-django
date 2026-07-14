from django.urls import path
from .presentation.views import DashboardView, TransactionHistoryView

app_name = 'dashboard'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
]