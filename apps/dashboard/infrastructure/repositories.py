from django.db import models
from apps.dashboard.models import Account, Transaction
from apps.core.domain.exceptions import NotFoundError

class AccountRepository:
    def get_user_accounts(self, user):
        return Account.objects.filter(user=user)

    def get_account_by_id(self, account_id, user=None):
        try:
            account = Account.objects.get(pk=account_id)
            if user and account.user != user:
                raise NotFoundError("Счет не найден.")
            return account
        except Account.DoesNotExist:
            raise NotFoundError("Счет не найден.")

class TransactionRepository:
    def get_transactions_for_account(self, account, limit=20):
        return Transaction.objects.filter(
            models.Q(from_account=account) | models.Q(to_account=account),
        ).order_by('-created_at')[:limit]