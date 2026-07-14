from apps.dashboard.infrastructure.repositories import TransactionRepository, AccountRepository

class DashboardService:
    def __init__(self, account_repo=None, transaction_repo=None):
        self.account_repo = account_repo or AccountRepository()
        self.transaction_repo = transaction_repo or TransactionRepository()

    def get_dashboard_data(self, user):
        accounts = self.account_repo.get_user_accounts(user)
        data = []
        for acc in accounts:
            data.append({
                'id': acc.id,
                'name': acc.name,
                'currency': acc.currency.code,
                'balance': str(acc.balance),
            })
        return {'accounts': data}

    def get_transactions(self, user, account_id, limit=20):
        account = self.account_repo.get_account_by_id(account_id, user)
        transactions = self.transaction_repo.get_transactions_for_account(account, limit)
        result = []
        for tx in transactions:
            result.append({
                'id': tx.id,
                'type': tx.transaction_type,
                'amount': str(tx.amount),
                'from_account': tx.from_account_id,
                'to_account': tx.to_account_id,
                'description': tx.description,
                'date': tx.created_at.isoformat(),
            })
        return result