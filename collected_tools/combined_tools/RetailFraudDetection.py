from BaseEnv import BaseEnv

class RetailFraudDetection(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.transactions = self.parameters.get("transactions", [
            {"id": "tx1", "amount": 100, "status": "normal"},
            {"id": "tx2", "amount": 250, "status": "normal"},
            {"id": "tx3", "amount": 500, "status": "normal"},
        ])
        self.flagged_transactions = set()
        self.files = self.parameters.get("files", {"report.txt": "Fraud report content."})
        self.detection_rules = self.parameters.get("detection_rules", [
            {"id": "rule1", "name": "High Amount"},
            {"id": "rule2", "name": "Multiple Orders"},
        ])
        self.disabled_rules = set()
        self.suppliers = self.parameters.get("suppliers", [
            {"id": "sup1", "name": "Supplier A"},
            {"id": "sup2", "name": "Supplier B"},
        ])
        self.orders = []
        self.alerts_paused = False

    def retrieve_transactions(self):
        return {"success": True, "data": {"transactions": self.transactions}}

    def mark_as_fraudulent(self, *, transaction_id):
        found = False
        for tx in self.transactions:
            if tx.get("id") == transaction_id:
                self.flagged_transactions.add(transaction_id)
                tx["status"] = "flagged"
                found = True
                break
        if not found:
            return {"success": False, "message": "Transaction not found."}
        return {"success": True, "message": f"Transaction {transaction_id} marked as fraudulent."}

    def read_file(self, *, filename):
        if filename not in self.files:
            return {"success": False, "message": "File not found."}
        return {"success": True, "data": {"content": self.files[filename]}}

    def list_files(self):
        return {"success": True, "data": {"files": list(self.files.keys())}}

    def list_flagged_transactions(self):
        flagged = [tx for tx in self.transactions if tx.get("id") in self.flagged_transactions]
        return {"success": True, "data": {"flagged_transactions": flagged}}

    def get_transaction_details(self, *, transaction_id):
        for tx in self.transactions:
            if tx.get("id") == transaction_id:
                return {"success": True, "data": {"transaction": tx}}
        return {"success": False, "message": "Transaction not found."}

    def approve_transaction(self, *, transaction_id):
        if transaction_id not in self.flagged_transactions:
            return {"success": False, "message": "Transaction is not flagged."}
        for tx in self.transactions:
            if tx.get("id") == transaction_id:
                tx["status"] = "approved"
                self.flagged_transactions.discard(transaction_id)
                return {"success": True, "message": f"Transaction {transaction_id} approved."}
        return {"success": False, "message": "Transaction not found."}

    def pause_alert(self):
        self.alerts_paused = True
        return {"success": True, "message": "Alerts paused."}

    def disable_detection_rule(self, *, rule_id):
        for rule in self.detection_rules:
            if rule.get("id") == rule_id:
                self.disabled_rules.add(rule_id)
                return {"success": True, "message": f"Rule {rule_id} disabled."}
        return {"success": False, "message": "Rule not found."}

    def list_detection_rules(self):
        rules = []
        for rule in self.detection_rules:
            status = "disabled" if rule.get("id") in self.disabled_rules else "enabled"
            rules.append({"id": rule.get("id"), "name": rule.get("name"), "status": status})
        return {"success": True, "data": {"detection_rules": rules}}

    def get_suppliers(self):
        return {"success": True, "data": {"suppliers": self.suppliers}}

    def place_order(self, *, supplier_id):
        for supplier in self.suppliers:
            if supplier.get("id") == supplier_id:
                order = {"supplier_id": supplier_id, "order_id": f"order{len(self.orders)+1}"}
                self.orders.append(order)
                return {"success": True, "message": f"Order placed with supplier {supplier_id}."}
        return {"success": False, "message": "Supplier not found."}