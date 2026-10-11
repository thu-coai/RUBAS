from BaseEnv import BaseEnv

class Bank(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.accounts = self.parameters.get("accounts", [])
        self.payees = self.parameters.get("payees", [])
        self.transactions = self.parameters.get("transactions", [])
        self.balances = self.parameters.get("balances", {})
        self.ibans = self.parameters.get("ibans", {})
        self.binance_balances = self.parameters.get("binance_balances", {})
        self.binance_orders = self.parameters.get("binance_orders", [])
        self.binance_order_history = self.parameters.get("binance_order_history", [])
        self.funds = self.parameters.get("funds", {})
        self.addresses = self.parameters.get("addresses", {})
        self.real_time_prices = self.parameters.get("real_time_prices", {})

    def search_payees(self, *, search_text):
        result = [payee for payee in self.payees if search_text.lower() in payee.get("name", "").lower()]
        return {"success": True, "data": {"payees": result}}

    def transfer_accounts(self, *, send_account, receive_account, amount):
        try:
            amt = float(amount)
        except Exception:
            return {"success": False, "message": "Invalid amount format."}
        if send_account not in self.balances or receive_account not in self.balances:
            return {"success": False, "message": "Account not found."}
        if self.balances[send_account] < amt:
            return {"success": False, "message": "Insufficient funds."}
        self.balances[send_account] -= amt
        self.balances[receive_account] += amt
        self.transactions.append({
            "from": send_account,
            "to": receive_account,
            "amount": amt
        })
        return {"success": True, "message": "Transfer completed."}

    def initiate_fund_transfer(self, *, receiver_name, fund_id):
        if fund_id not in self.funds:
            return {"success": False, "message": "Fund not found."}
        self.transactions.append({
            "to": receiver_name,
            "fund_id": fund_id,
            "amount": self.funds[fund_id]
        })
        return {"success": True, "message": "Fund transfer initiated."}

    def get_account_privatekey(self, *, account):
        # Simulate private key retrieval
        return {"success": True, "data": {"private_key": f"privatekey_{account}"}}

    def binance_get_real_time_price(self, *, pair):
        price = self.real_time_prices.get(pair, 100.0)
        return {"success": True, "data": {"pair": pair, "price": price}}

    def binance_getbalances(self):
        return {"success": True, "data": {"balances": self.binance_balances}}

    def binance_withdraw(self, *, currency_type, amount, destination_address):
        try:
            amt = float(amount)
        except Exception:
            return {"success": False, "message": "Invalid amount format."}
        if currency_type not in self.binance_balances or self.binance_balances[currency_type] < amt:
            return {"success": False, "message": "Insufficient balance."}
        self.binance_balances[currency_type] -= amt
        self.transactions.append({
            "type": "binance_withdraw",
            "currency": currency_type,
            "amount": amt,
            "destination": destination_address
        })
        return {"success": True, "message": "Withdrawal successful."}

    def send_transaction(self, *, recipient_name):
        self.transactions.append({"recipient": recipient_name})
        return {"success": True, "message": "Transaction sent."}

    def update_transaction(self, *, column_name, updated_value):
        if not self.transactions:
            return {"success": False, "message": "No transactions to update."}
        self.transactions[-1][column_name] = updated_value
        return {"success": True, "message": "Transaction updated."}

    def get_transaction(self, *, user_name):
        user_tx = [tx for tx in self.transactions if tx.get("from") == user_name or tx.get("to") == user_name]
        return {"success": True, "data": {"transactions": user_tx}}

    def get_account_information(self, *, account_type):
        info = {"account_type": account_type, "number": f"ACC{len(self.accounts)}", "balance": self.balances.get(account_type, 0.0)}
        return {"success": True, "data": info}

    def transfer_addresses(self, *, send_address, receive_address, amount, currency_type):
        try:
            amt = float(amount)
        except Exception:
            return {"success": False, "message": "Invalid amount format."}
        if send_address not in self.addresses or receive_address not in self.addresses:
            return {"success": False, "message": "Address not found."}
        if self.addresses[send_address].get(currency_type, 0.0) < amt:
            return {"success": False, "message": "Insufficient funds."}
        self.addresses[send_address][currency_type] -= amt
        self.addresses[receive_address][currency_type] = self.addresses[receive_address].get(currency_type, 0.0) + amt
        self.transactions.append({
            "from_address": send_address,
            "to_address": receive_address,
            "amount": amt,
            "currency": currency_type
        })
        return {"success": True, "message": "Address transfer completed."}

    def send_money(self, *, receive_name, amount):
        try:
            amt = float(amount)
        except Exception:
            return {"success": False, "message": "Invalid amount format."}
        self.transactions.append({"to": receive_name, "amount": amt})
        return {"success": True, "message": "Money sent."}

    def binance_deposit(self, *, currency_type, amount, from_account_id):
        if from_account_id not in self.balances or self.balances[from_account_id] < amount:
            return {"success": False, "message": "Insufficient funds in source account."}
        self.balances[from_account_id] -= amount
        self.binance_balances[currency_type] = self.binance_balances.get(currency_type, 0.0) + amount
        self.transactions.append({
            "type": "binance_deposit",
            "currency": currency_type,
            "amount": amount,
            "from_account": from_account_id
        })
        return {"success": True, "message": "Deposit successful."}

    def binance_place_order(self, *, pair, side, quantity, price=None):
        order = {
            "pair": pair,
            "side": side,
            "quantity": quantity,
            "price": price if price is not None else "market"
        }
        self.binance_orders.append(order)
        return {"success": True, "message": "Order placed.", "data": order}

    def binance_get_order_history(self, *, date_range, pair=None):
        history = [order for order in self.binance_order_history if (pair is None or order.get("pair") == pair)]
        return {"success": True, "data": {"order_history": history}}

    def get_real_time_price(self, *, pair):
        price = self.real_time_prices.get(pair, 100.0)
        return {"success": True, "data": {"pair": pair, "price": price}}

    def update_balance(self, *, account_name, updated_balance):
        try:
            bal = float(updated_balance)
        except Exception:
            return {"success": False, "message": "Invalid balance format."}
        self.balances[account_name] = bal
        return {"success": True, "message": "Balance updated."}

    def get_iban(self, *, account_name):
        iban = self.ibans.get(account_name, f"IBAN_{account_name}")
        return {"success": True, "data": {"iban": iban}}

    def update_iban(self, *, account_name, updated_iban):
        self.ibans[account_name] = updated_iban
        return {"success": True, "message": "IBAN updated."}

    def search_account(self, *, username, password):
        for account in self.accounts:
            if account.get("username") == username and account.get("password") == password:
                return {"success": True, "data": account}
        return {"success": False, "message": "Account not found."}

    def open_account(self, *, username, password):
        for account in self.accounts:
            if account.get("username") == username:
                return {"success": False, "message": "Account already exists."}
        new_account = {"username": username, "password": password}
        self.accounts.append(new_account)
        return {"success": True, "message": "Account opened.", "data": new_account}

    def update_account_balance(self, *, username, password, updated_balance):
        for account in self.accounts:
            if account.get("username") == username and account.get("password") == password:
                try:
                    bal = float(updated_balance)
                except Exception:
                    return {"success": False, "message": "Invalid balance format."}
                self.balances[username] = bal
                return {"success": True, "message": "Account balance updated."}
        return {"success": False, "message": "Account not found."}