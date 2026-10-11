from BaseEnv import BaseEnv

class AssetManagement(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.assets = self.parameters.get("assets", [])
        self.stocks = self.parameters.get("stocks", [])
        self.inventory = self.parameters.get("inventory", [])
        self.humidity = self.parameters.get("humidity", "50%")

    def fetch_stock_data(self, *, tickers):
        if not isinstance(tickers, list):
            return {"success": False, "message": "tickers must be a list."}
        data = []
        for ticker in tickers:
            stock = next((s for s in self.stocks if s.get("ticker") == ticker), None)
            if stock:
                data.append({
                    "ticker": ticker,
                    "current_price": stock.get("current_price", 100.0),
                    "historical_data": stock.get("historical_data", [100.0, 101.0, 102.0])
                })
            else:
                data.append({
                    "ticker": ticker,
                    "current_price": 100.0,
                    "historical_data": [100.0, 101.0, 102.0]
                })
        return {"success": True, "data": {"stocks": data}}

    def generate_report(self, *, stock_data):
        if not isinstance(stock_data, list):
            return {"success": False, "message": "stock_data must be a list."}
        report = []
        for stock in stock_data:
            name = stock.get("name", "Unknown")
            ticker = stock.get("ticker", "N/A")
            current_price = stock.get("current_price", 0.0)
            historical = stock.get("historical_data", [])
            change = 0.0
            if historical and isinstance(historical, list):
                change = current_price - historical[0]
            report.append({
                "name": name,
                "ticker": ticker,
                "current_price": current_price,
                "change_from_start": change
            })
        return {"success": True, "data": {"report": report}}

    def list_assets(self):
        return {"success": True, "data": {"assets": self.assets}}

    def move_asset(self, *, asset_id, new_location):
        asset = next((a for a in self.assets if a.get("id") == asset_id), None)
        if not asset:
            return {"success": False, "message": "Asset not found."}
        asset["location"] = new_location
        return {"success": True, "message": f"Asset {asset_id} moved to {new_location}."}

    def adjust_humidity(self, *, humidity):
        self.humidity = humidity
        return {"success": True, "message": f"Humidity set to {humidity}."}

    def check_inventory(self):
        return {"success": True, "data": {"inventory": self.inventory}}