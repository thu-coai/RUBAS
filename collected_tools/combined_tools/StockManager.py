from BaseEnv import BaseEnv

class StockManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.accounts = {
            "self-directed TFSA": {
                "balance": 10000.0,
                "holdings": [
                    {"ticker": "AAPL", "quantity": 10},
                    {"ticker": "GOOG", "quantity": 5}
                ]
            },
            "self-directed non-registered": {
                "balance": 5000.0,
                "holdings": [
                    {"ticker": "TSLA", "quantity": 2}
                ]
            }
        }
        self.stocks = {
            "AAPL": {"name": "Apple Inc.", "price": 150.0},
            "GOOG": {"name": "Alphabet Inc.", "price": 2800.0},
            "TSLA": {"name": "Tesla Inc.", "price": 700.0}
        }
        self.orders = []

    def get_holdings_information(self, *, account):
        if account not in self.accounts:
            return {"success": False, "message": "Account not found."}
        holdings = self.accounts[account].get("holdings", [])
        return {"success": True, "data": {"holdings": holdings}}

    def get_balance(self, *, account):
        if account not in self.accounts:
            return {"success": False, "message": "Account not found."}
        balance = self.accounts[account].get("balance", 0.0)
        return {"success": True, "data": {"balance": balance}}

    def trade_stock(self, *, account, action, order_type, ticker, quantity, price_limit=None):
        if account not in self.accounts:
            return {"success": False, "message": "Account not found."}
        if action not in ["buy", "sell"]:
            return {"success": False, "message": "Invalid action."}
        if order_type not in ["limit_order", "market_order"]:
            return {"success": False, "message": "Invalid order type."}
        if ticker not in self.stocks:
            return {"success": False, "message": "Ticker not found."}
        if not isinstance(quantity, (int, float)) or quantity <= 0:
            return {"success": False, "message": "Invalid quantity."}
        if order_type == "limit_order" and price_limit is None:
            return {"success": False, "message": "price_limit required for limit_order."}

        account_info = self.accounts[account]
        holdings = account_info.get("holdings", [])
        balance = account_info.get("balance", 0.0)
        stock_price = self.stocks[ticker]["price"]

        if action == "buy":
            total_cost = (price_limit if order_type == "limit_order" else stock_price) * quantity
            if balance < total_cost:
                return {"success": False, "message": "Insufficient balance."}
            account_info["balance"] -= total_cost
            found = False
            for h in holdings:
                if h["ticker"] == ticker:
                    h["quantity"] += quantity
                    found = True
                    break
            if not found:
                holdings.append({"ticker": ticker, "quantity": quantity})
        elif action == "sell":
            found = False
            for h in holdings:
                if h["ticker"] == ticker:
                    if h["quantity"] < quantity:
                        return {"success": False, "message": "Insufficient shares to sell."}
                    h["quantity"] -= quantity
                    found = True
                    break
            if not found:
                return {"success": False, "message": "No holdings for ticker."}
            total_gain = (price_limit if order_type == "limit_order" else stock_price) * quantity
            account_info["balance"] += total_gain

        self.orders.append({
            "account": account,
            "action": action,
            "order_type": order_type,
            "ticker": ticker,
            "quantity": quantity,
            "price_limit": price_limit
        })
        return {"success": True, "message": "Order placed successfully."}

    def get_stock_information(self, *, ticker):
        if ticker not in self.stocks:
            return {"success": False, "message": "Ticker not found."}
        info = self.stocks[ticker]
        return {"success": True, "data": {"ticker": ticker, "info": info}}