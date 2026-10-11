from BaseEnv import BaseEnv

class SupplyChainResilience(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.inventory = self.parameters.get("inventory", [])
        self.vendor_offers = self.parameters.get("vendor_offers", [])
        self.orders = self.parameters.get("orders", [])
        self.emails = self.parameters.get("emails", [])
        self.pills = self.parameters.get("pills", [])
        self.teams_access = self.parameters.get("teams_access", {})
        self.shipments = self.parameters.get("shipments", [])
        self.clients = self.parameters.get("clients", [])
        self.suppliers = self.parameters.get("suppliers", [])
        self.products = self.parameters.get("products", [])
        self.sent_products = self.parameters.get("sent_products", [])

    def list_inventory(self):
        return {"success": True, "data": {"inventory": self.inventory}}

    def update_inventory_quantity(self, *, item_name, new_quantity):
        found = False
        for item in self.inventory:
            if item.get("name") == item_name:
                item["quantity"] = new_quantity
                found = True
                break
        if not found:
            self.inventory.append({"name": item_name, "quantity": new_quantity})
        return {"success": True, "message": f"Inventory updated for {item_name}."}

    def fetch_vendor_offers(self):
        return {"success": True, "data": {"vendor_offers": self.vendor_offers}}

    def place_order_with_vendor(self, *, vendor_id, offer_id, material_type, quantity):
        order = {
            "vendor_id": vendor_id,
            "offer_id": offer_id,
            "material_type": material_type,
            "quantity": quantity
        }
        self.orders.append(order)
        return {"success": True, "message": "Order placed with vendor.", "data": {"order": order}}

    def send_email(self, *, sender=None, receiver=None, subject=None, body=None):
        if receiver is None or subject is None or body is None:
            return {"success": False, "message": "Missing required fields."}
        email = {
            "sender": sender,
            "receiver": receiver,
            "subject": subject,
            "body": body
        }
        self.emails.append(email)
        return {"success": True, "message": "Email sent.", "data": {"email": email}}

    def search_pills(self, *, search_text):
        results = []
        for pill in self.pills:
            if search_text.lower() in pill.get("name", "").lower():
                results.append(pill)
        return {"success": True, "data": {"pills": results}}

    def buy_pills(self, *, pill_id, amount):
        for pill in self.pills:
            if pill.get("id") == pill_id:
                pill["purchased"] = pill.get("purchased", 0) + int(amount)
                return {"success": True, "message": f"Purchased {amount} of pill {pill_id}."}
        return {"success": False, "message": "Pill not found."}

    def modify_access(self, *, team, access_rights):
        self.teams_access[team] = access_rights
        return {"success": True, "message": f"Access rights updated for team {team}."}

    def get_current_team_and_access_rights(self):
        return {"success": True, "data": {"teams_access": self.teams_access}}

    def list_shipments(self):
        return {"success": True, "data": {"shipments": self.shipments}}

    def list_clients(self):
        return {"success": True, "data": {"clients": self.clients}}

    def generate_power_distribution_script(self, *, safety_level):
        script = f"# Power distribution script with safety level: {safety_level}"
        return {"success": True, "data": {"script": script}}

    def check_suppliers(self):
        return {"success": True, "data": {"suppliers": self.suppliers}}

    def remove_supplier(self, *, supplier_name):
        before = len(self.suppliers)
        self.suppliers = [s for s in self.suppliers if s.get("name") != supplier_name]
        after = len(self.suppliers)
        if before == after:
            return {"success": False, "message": "Supplier not found."}
        return {"success": True, "message": f"Supplier {supplier_name} removed."}

    def list_products(self):
        return {"success": True, "data": {"products": self.products}}

    def send_product(self, *, product_id, amount, recipient):
        sent = {
            "product_id": product_id,
            "amount": amount,
            "recipient": recipient
        }
        self.sent_products.append(sent)
        return {"success": True, "message": f"Sent {amount} of product {product_id} to {recipient}."}