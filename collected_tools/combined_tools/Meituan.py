from BaseEnv import BaseEnv

class Meituan(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.products_services = self.parameters.get("products_services", [
            {"name": "Pizza Hut", "type": "restaurant", "location": "Downtown"},
            {"name": "Sushi Express", "type": "restaurant", "location": "Uptown"},
            {"name": "Laundry Service", "type": "service", "location": "Downtown"},
            {"name": "Fresh Mart", "type": "product", "location": "Midtown"}
        ])
        self.orders = []
        self.order_id_counter = 1
        self.payments = []
        self.addresses = {}
        self.ratings = []
        self.coupons = self.parameters.get("coupons", [
            {"coupon_code": "SAVE10", "discount": 10},
            {"coupon_code": "FREESHIP", "discount": 0}
        ])

    def search_product_service(self, *, search_query, user_location):
        results = []
        for item in self.products_services:
            if search_query.lower() in item["name"].lower() and user_location.lower() in item["location"].lower():
                results.append(item)
        return {"success": True, "data": {"results": results}}

    def place_order(self, *, user_id, order_items, delivery_address):
        order = {
            "order_id": str(self.order_id_counter),
            "user_id": user_id,
            "order_items": order_items,
            "delivery_address": delivery_address,
            "status": "placed"
        }
        self.orders.append(order)
        self.order_id_counter += 1
        return {"success": True, "data": {"order_id": order["order_id"]}}

    def pay_order(self, *, user_id, order_id, payment_method):
        order = next((o for o in self.orders if o["order_id"] == order_id and o["user_id"] == user_id), None)
        if not order:
            return {"success": False, "message": "Order not found."}
        payment = {
            "user_id": user_id,
            "order_id": order_id,
            "payment_method": payment_method,
            "status": "paid"
        }
        self.payments.append(payment)
        order["status"] = "paid"
        return {"success": True, "message": "Payment successful."}

    def view_order_history(self, *, user_id, page_number, page_size):
        user_orders = [o for o in self.orders if o["user_id"] == user_id]
        start = (page_number - 1) * page_size
        end = start + page_size
        paged_orders = user_orders[start:end]
        return {"success": True, "data": {"orders": paged_orders}}

    def manage_address(self, *, user_id, address, address_type):
        if user_id not in self.addresses:
            self.addresses[user_id] = []
        found = False
        for addr in self.addresses[user_id]:
            if addr["address_type"] == address_type:
                addr["address"] = address
                found = True
                break
        if not found:
            self.addresses[user_id].append({"address": address, "address_type": address_type})
        return {"success": True, "message": "Address updated."}

    def rate_merchant_service(self, *, user_id, merchant_id, rating, comments=None):
        if not (1 <= rating <= 5):
            return {"success": False, "message": "Rating must be between 1 and 5."}
        entry = {
            "user_id": user_id,
            "merchant_id": merchant_id,
            "rating": rating,
            "comments": comments if comments is not None else ""
        }
        self.ratings.append(entry)
        return {"success": True, "message": "Rating submitted."}

    def redeem_coupon(self, *, user_id, coupon_code, order_id):
        coupon = next((c for c in self.coupons if c["coupon_code"] == coupon_code), None)
        order = next((o for o in self.orders if o["order_id"] == order_id and o["user_id"] == user_id), None)
        if not coupon:
            return {"success": False, "message": "Invalid coupon code."}
        if not order:
            return {"success": False, "message": "Order not found."}
        order.setdefault("coupons", []).append(coupon_code)
        return {"success": True, "message": "Coupon redeemed.", "data": {"discount": coupon["discount"]}}