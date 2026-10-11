from BaseEnv import BaseEnv

class ProductManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.products = self.parameters.get("products", [
            {"name": "Apple", "price": "$1"},
            {"name": "Banana", "price": "$0.5"},
            {"name": "Carrot", "price": "$0.3"}
        ])
        self.market_info = self.parameters.get("market_info", [
            {"product": "Apple", "trend": "up", "last_price": "$1"},
            {"product": "Banana", "trend": "stable", "last_price": "$0.5"},
            {"product": "Carrot", "trend": "down", "last_price": "$0.3"}
        ])

    def list_products(self):
        return {"success": True, "data": {"products": self.products}}

    def update_product_price(self, *, product_name, new_price):
        found = False
        for product in self.products:
            if product.get("name") == product_name:
                product["price"] = new_price
                found = True
                break
        if found:
            return {"success": True, "message": f"Price for '{product_name}' updated to {new_price}."}
        else:
            return {"success": False, "message": f"Product '{product_name}' not found."}

    def view_market_information(self):
        return {"success": True, "data": {"market_info": self.market_info}}