from BaseEnv import BaseEnv

class Webshop(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.items = self.parameters.get("items", [
            {"id": "item1", "name": "T-shirt", "price": 19.99, "quantity": 100, "description": "A comfortable cotton T-shirt."},
            {"id": "item2", "name": "Jeans", "price": 49.99, "quantity": 50, "description": "Classic blue jeans."},
            {"id": "item3", "name": "Sneakers", "price": 89.99, "quantity": 30, "description": "Stylish sneakers."}
        ])
        self.cart = []
        self.saved_addresses = self.parameters.get("saved_addresses", [
            {"name": "Alice", "phone_number": "1234567890", "address": "123 Main St"}
        ])
        self.saved_payment_methods = self.parameters.get("saved_payment_methods", [
            {"card_number": "4111111111111111", "expiry_date": "12/25", "cvv": "123"}
        ])
        self.orders = []

    def add_to_cart(self, *, item_id, quantity):
        if not isinstance(item_id, str) or not isinstance(quantity, int):
            return {"success": False, "message": "Invalid item_id or quantity type."}
        item = next((i for i in self.items if i["id"] == item_id), None)
        if not item:
            return {"success": False, "message": "Item not found."}
        if quantity <= 0:
            return {"success": False, "message": "Quantity must be positive."}
        if item["quantity"] < quantity:
            return {"success": False, "message": "Not enough stock."}
        cart_item = next((c for c in self.cart if c["item_id"] == item_id), None)
        if cart_item:
            cart_item["quantity"] += quantity
        else:
            self.cart.append({"item_id": item_id, "quantity": quantity})
        item["quantity"] -= quantity
        return {"success": True, "message": "Item added to cart."}

    def place_order(self, *, shipping_address, payment_method):
        if not self.cart:
            return {"success": False, "message": "Cart is empty."}
        if shipping_address is None:
            if self.saved_addresses:
                shipping_address = self.saved_addresses[0]
            else:
                return {"success": False, "message": "No saved address available."}
        if payment_method is None:
            if self.saved_payment_methods:
                payment_method = self.saved_payment_methods[0]
            else:
                return {"success": False, "message": "No saved payment method available."}
        order = {
            "items": list(self.cart),
            "shipping_address": shipping_address,
            "payment_method": payment_method
        }
        self.orders.append(order)
        self.cart.clear()
        return {"success": True, "message": "Order placed successfully.", "data": {"order": order}}

    def view_saved_addresses(self):
        return {"success": True, "data": {"addresses": self.saved_addresses}}

    def view_saved_payment_methods(self):
        return {"success": True, "data": {"payment_methods": self.saved_payment_methods}}

    def get_item_details(self, *, item_id):
        item = next((i for i in self.items if i["id"] == item_id), None)
        if not item:
            return {"success": False, "message": "Item not found."}
        return {"success": True, "data": {"item": item}}

    def search_items(self, *, search_text):
        if not isinstance(search_text, str):
            return {"success": False, "message": "Invalid search_text type."}
        results = [i for i in self.items if search_text.lower() in i.get("name", "").lower() or search_text.lower() in i.get("description", "").lower()]
        return {"success": True, "data": {"items": results}}

    def update_item(self, *, item_id, quantity):
        item = next((i for i in self.items if i["id"] == item_id), None)
        if not item:
            return {"success": False, "message": "Item not found."}
        if not isinstance(quantity, (int, float)) or quantity < 0:
            return {"success": False, "message": "Invalid quantity."}
        item["quantity"] = quantity
        return {"success": True, "message": "Item quantity updated."}

    def update_item_price(self, *, item_id, price):
        item = next((i for i in self.items if i["id"] == item_id), None)
        if not item:
            return {"success": False, "message": "Item not found."}
        if not isinstance(price, (int, float)) or price < 0:
            return {"success": False, "message": "Invalid price."}
        item["price"] = price
        return {"success": True, "message": "Item price updated."}

    def delete_items(self, *, item_ids):
        if not isinstance(item_ids, list):
            return {"success": False, "message": "item_ids must be a list."}
        deleted = []
        for item_id in item_ids:
            item = next((i for i in self.items if i["id"] == item_id), None)
            if item:
                self.items.remove(item)
                deleted.append(item_id)
        return {"success": True, "message": "Items deleted.", "data": {"deleted_item_ids": deleted}}