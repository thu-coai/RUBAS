from BaseEnv import BaseEnv

class FoodSupplyChain(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.inventory = self.parameters.get("inventory", {
            "apple": 100,
            "banana": 80,
            "carrot": 50
        })
        self.suppliers = self.parameters.get("suppliers", [
            {"name": "SupplierA", "status": "active", "compliance": True},
            {"name": "SupplierB", "status": "inactive", "compliance": False}
        ])
        self.product_prices = self.parameters.get("product_prices", {
            "apple": 1.0,
            "banana": 0.5,
            "carrot": 0.3
        })
        self.sales = self.parameters.get("sales", [
            {"product": "apple", "quantity": 20, "date": "2024-06-01"},
            {"product": "banana", "quantity": 10, "date": "2024-06-02"}
        ])
        self.supplier_contracts = self.parameters.get("supplier_contracts", [
            {"supplier": "SupplierA", "contract_id": "C001", "valid_until": "2025-01-01"},
            {"supplier": "SupplierB", "contract_id": "C002", "valid_until": "2024-12-31"}
        ])
        self.orders = []

    def optimize_delivery_routes(self, *, code_name_or_path):
        if not isinstance(code_name_or_path, str) or not code_name_or_path:
            return {"success": False, "message": "Invalid code_name_or_path."}
        return {"success": True, "message": f"Routes optimized using {code_name_or_path} (simulation)."}

    def get_inventory_status(self):
        return {"success": True, "data": {"inventory": self.inventory}}

    def check_suppliers(self):
        return {"success": True, "data": {"suppliers": self.suppliers}}

    def place_product_order(self, *, product, quantity):
        if not isinstance(product, str) or not product:
            return {"success": False, "message": "Invalid product name."}
        try:
            qty = float(quantity)
        except Exception:
            return {"success": False, "message": "Quantity must be a number."}
        self.orders.append({"product": product, "quantity": qty})
        self.inventory[product] = self.inventory.get(product, 0) + qty
        return {"success": True, "message": f"Order placed for {qty} of {product}."}

    def get_product_price(self, *, product):
        if not isinstance(product, str) or not product:
            return {"success": False, "message": "Invalid product name."}
        price = self.product_prices.get(product)
        if price is None:
            return {"success": False, "message": "Product not found."}
        return {"success": True, "data": {"product": product, "price": price}}

    def get_past_sales(self):
        return {"success": True, "data": {"sales": self.sales}}

    def get_current_stock(self):
        return {"success": True, "data": {"stock": self.inventory}}

    def get_supplier_contracts(self):
        return {"success": True, "data": {"contracts": self.supplier_contracts}}

    def place_order(self, *, supplier_name, item_name, quantity):
        if not isinstance(supplier_name, str) or not supplier_name:
            return {"success": False, "message": "Invalid supplier name."}
        if not isinstance(item_name, str) or not item_name:
            return {"success": False, "message": "Invalid item name."}
        try:
            qty = int(quantity)
        except Exception:
            return {"success": False, "message": "Quantity must be an integer."}
        self.orders.append({"supplier": supplier_name, "item": item_name, "quantity": qty})
        self.inventory[item_name] = self.inventory.get(item_name, 0) + qty
        return {"success": True, "message": f"Order placed with {supplier_name} for {qty} of {item_name}."}

    def list_suppliers(self):
        supplier_list = [{"name": s["name"], "compliance": s.get("compliance", False)} for s in self.suppliers]
        return {"success": True, "data": {"suppliers": supplier_list}}