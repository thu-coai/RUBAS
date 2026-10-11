from BaseEnv import BaseEnv

class FinancialManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.users = self.parameters.get("users", [])
        self.accounts = self.parameters.get("accounts", [])
        self.financial_data = self.parameters.get("financial_data", {})
        self.verified_users = set()

    def verify_user_identity(self, *, user_id):
        for user in self.users:
            if user.get("id") == user_id:
                self.verified_users.add(user_id)
                return {"success": True, "message": f"User {user_id} verified."}
        return {"success": False, "message": f"User {user_id} not found."}

    def transfer_money(self, *, src_account, dst_account, amount):
        try:
            amt = float(amount)
        except Exception:
            return {"success": False, "message": "Invalid amount format."}
        src = None
        dst = None
        for acc in self.accounts:
            if acc.get("id") == src_account:
                src = acc
            if acc.get("id") == dst_account:
                dst = acc
        if src is None or dst is None:
            return {"success": False, "message": "Source or destination account not found."}
        if src.get("balance", 0) < amt:
            return {"success": False, "message": "Insufficient funds in source account."}
        src["balance"] -= amt
        dst["balance"] = dst.get("balance", 0) + amt
        return {"success": True, "message": f"Transferred {amt} from {src_account} to {dst_account}."}

    def retrieve_financial_data(self):
        return {"success": True, "data": self.financial_data}