from django.urls import path
from .presentation.views import DashboardView, TransactionHistoryView, CreateAccountView, CreateTransferView

app_name = 'dashboard'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
    path('create/', CreateAccountView.as_view(), name='create_account'),
    path('transfer/', CreateTransferView.as_view(), name='create_transfer'),
]