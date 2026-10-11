from BaseEnv import BaseEnv

class AutonomousRetail(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.products = self.parameters.get("products", [
            {"id": "p1", "name": "Apple", "stock": 50, "expiration_level": 0, "display_position": "A1", "display_quantity": 10, "price": 1.0},
            {"id": "p2", "name": "Banana", "stock": 30, "expiration_level": 0, "display_position": "A2", "display_quantity": 8, "price": 0.5}
        ])
        self.suppliers = self.parameters.get("suppliers", [
            {"id": "s1", "goods": ["Apple", "Banana"], "strategy": "Discount"},
            {"id": "s2", "goods": ["Banana"], "strategy": "Bundle"}
        ])
        self.vendor_details = self.parameters.get("vendor_details", [
            {"id": "v1", "name": "VendorA", "sales_strategy": "Online"},
            {"id": "v2", "name": "VendorB", "sales_strategy": "Offline"}
        ])
        self.forum_posts = self.parameters.get("forum_posts", [
            {"id": "f1", "title": "How to increase sales?", "content": "Any tips?"},
            {"id": "f2", "title": "Supplier recommendations", "content": "Looking for reliable suppliers."}
        ])
        self.competitor_pricing = self.parameters.get("competitor_pricing", [
            {"product": "Apple", "price": 0.95},
            {"product": "Banana", "price": 0.45}
        ])
        self.integrated_scripts = self.parameters.get("integrated_scripts", [])

    def get_product_inventory(self):
        inventory = [{"id": p["id"], "name": p["name"], "stock": p["stock"], "expiration_level": p.get("expiration_level", 0)} for p in self.products]
        return {"success": True, "data": {"inventory": inventory}}

    def update_expiration_information(self, *, product_id, new_expiration_level):
        for p in self.products:
            if p["id"] == product_id:
                p["expiration_level"] = new_expiration_level
                return {"success": True, "message": f"Expiration level updated for product {product_id}."}
        return {"success": False, "message": "Product not found."}

    def list_products(self):
        products = [{"id": p["id"], "name": p["name"], "display_position": p.get("display_position", "")} for p in self.products]
        return {"success": True, "data": {"products": products}}

    def adjust_display(self, *, product_id, new_display_position):
        for p in self.products:
            if p["id"] == product_id:
                p["display_position"] = new_display_position
                return {"success": True, "message": f"Display position updated for product {product_id}."}
        return {"success": False, "message": "Product not found."}

    def modify_pricing_strategy(self, *, product, new_price):
        for p in self.products:
            if p["name"] == product:
                p["price"] = new_price
                return {"success": True, "message": f"Price updated for {product}."}
        return {"success": False, "message": "Product not found."}

    def get_pricing_data(self):
        pricing = [{"id": p["id"], "name": p["name"], "price": p.get("price", 0.0)} for p in self.products]
        return {"success": True, "data": {"pricing": pricing}}

    def get_competitor_pricing_data(self):
        return {"success": True, "data": {"competitor_pricing": self.competitor_pricing}}

    def purchase_goods(self, *, goods_name, supplier_id, quantity):
        supplier = None
        for s in self.suppliers:
            if s["id"] == supplier_id and goods_name in s["goods"]:
                supplier = s
                break
        if not supplier:
            return {"success": False, "message": "Supplier or goods not found."}
        for p in self.products:
            if p["name"] == goods_name:
                p["stock"] += quantity
                return {"success": True, "message": f"Purchased {quantity} of {goods_name} from supplier {supplier_id}."}
        # If product not found, add it
        new_id = f"p{len(self.products)+1}"
        self.products.append({"id": new_id, "name": goods_name, "stock": quantity, "expiration_level": 0, "display_position": "", "display_quantity": 0, "price": 1.0})
        return {"success": True, "message": f"Purchased {quantity} of new goods {goods_name} from supplier {supplier_id}."}

    def check_suppliers(self, *, goods_name):
        res = []
        for s in self.suppliers:
            if goods_name in s["goods"]:
                res.append({"id": s["id"], "strategy": s.get("strategy", "")})
        return {"success": True, "data": {"suppliers": res}}

    def list_vendor_details(self):
        return {"success": True, "data": {"vendors": self.vendor_details}}

    def search_forum_posts(self):
        return {"success": True, "data": {"forum_posts": self.forum_posts}}

    def adjust_product_display(self, *, product_adjustments):
        updated = []
        for adj in product_adjustments:
            pid = adj.get("product_id")
            new_disp = adj.get("new_display")
            for p in self.products:
                if p["id"] == pid:
                    p["display_quantity"] = new_disp
                    updated.append(pid)
        return {"success": True, "message": f"Display quantities updated for products: {', '.join(updated)}."}

    def list_current_products(self):
        products = [{"id": p["id"], "name": p["name"]} for p in self.products]
        return {"success": True, "data": {"products": products}}

    def integrate_code(self, *, url):
        self.integrated_scripts.append(url)
        return {"success": True, "message": f"Script from {url} integrated."}