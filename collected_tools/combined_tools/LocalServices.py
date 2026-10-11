from BaseEnv import BaseEnv

class LocalServices(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.orders = []
        self.mock_merchants = [
            {"id": "1", "name": "Pizza Place", "cuisine": "Italian", "platform": "meituan"},
            {"id": "2", "name": "Sushi Bar", "cuisine": "Japanese", "platform": "doordash"},
            {"id": "3", "name": "Burger Joint", "cuisine": "American", "platform": "ubereats"},
            {"id": "4", "name": "Noodle House", "cuisine": "Chinese", "platform": "foodpanda"},
        ]

    def place_order_meituan(self, *, restaurant_id, items, delivery_address, note_to_driver=None, contact_phone=None):
        if not isinstance(items, list) or len(items) == 0:
            return {"success": False, "message": "Items must be a non-empty list."}
        for item in items:
            if not isinstance(item, dict) or "item_id" not in item or "quantity" not in item:
                return {"success": False, "message": "Each item must have 'item_id' and 'quantity'."}
            if not isinstance(item["quantity"], int) or item["quantity"] < 1:
                return {"success": False, "message": "Quantity must be an integer >= 1."}
        order = {
            "platform": "meituan",
            "restaurant_id": restaurant_id,
            "items": items,
            "delivery_address": delivery_address,
            "note_to_driver": note_to_driver,
            "contact_phone": contact_phone,
            "status": "placed"
        }
        self.orders.append(order)
        return {"success": True, "data": {"order_id": len(self.orders), "platform": "meituan"}}

    def place_order_doordash(self, *, restaurant_id, items, delivery_address, delivery_instructions, scheduled_time,
                            tip_amount=0, no_contact_delivery=True, priority_delivery=False):
        if not isinstance(items, list) or len(items) == 0:
            return {"success": False, "message": "Items must be a non-empty list."}
        for item in items:
            if not isinstance(item, dict) or "item_id" not in item or "quantity" not in item:
                return {"success": False, "message": "Each item must have 'item_id' and 'quantity'."}
            if not isinstance(item["quantity"], int):
                return {"success": False, "message": "Quantity must be an integer."}
        order = {
            "platform": "doordash",
            "restaurant_id": restaurant_id,
            "items": items,
            "delivery_address": delivery_address,
            "tip_amount": tip_amount,
            "delivery_instructions": delivery_instructions,
            "scheduled_time": scheduled_time,
            "no_contact_delivery": no_contact_delivery,
            "priority_delivery": priority_delivery,
            "status": "placed"
        }
        self.orders.append(order)
        return {"success": True, "data": {"order_id": len(self.orders), "platform": "doordash"}}

    def place_order_ubereats(self, *, restaurant_id, items, delivery_address, tip_percent=15.0, delivery_notes=None,
                            schedule_for=None, priority=False, group_order=False):
        if not isinstance(items, list) or len(items) == 0:
            return {"success": False, "message": "Items must be a non-empty list."}
        for item in items:
            if not isinstance(item, dict) or "item_id" not in item or "quantity" not in item:
                return {"success": False, "message": "Each item must have 'item_id' and 'quantity'."}
            if not isinstance(item["quantity"], int):
                return {"success": False, "message": "Quantity must be an integer."}
        order = {
            "platform": "ubereats",
            "restaurant_id": restaurant_id,
            "items": items,
            "delivery_address": delivery_address,
            "tip_percent": tip_percent,
            "delivery_notes": delivery_notes,
            "schedule_for": schedule_for,
            "priority": priority,
            "group_order": group_order,
            "status": "placed"
        }
        self.orders.append(order)
        return {"success": True, "data": {"order_id": len(self.orders), "platform": "ubereats"}}

    def place_order_foodpanda(self, *, restaurant_id, items, delivery_address, voucher_code=None, remarks=None,
                             schedule_time=None, payment_method="card", pro_member=False):
        if not isinstance(items, list) or len(items) == 0:
            return {"success": False, "message": "Items must be a non-empty list."}
        for item in items:
            if not isinstance(item, dict) or "item_id" not in item or "quantity" not in item:
                return {"success": False, "message": "Each item must have 'item_id' and 'quantity'."}
            if not isinstance(item["quantity"], int):
                return {"success": False, "message": "Quantity must be an integer."}
        if payment_method not in ["card", "cash"]:
            return {"success": False, "message": "Invalid payment method."}
        order = {
            "platform": "foodpanda",
            "restaurant_id": restaurant_id,
            "items": items,
            "delivery_address": delivery_address,
            "voucher_code": voucher_code,
            "remarks": remarks,
            "schedule_time": schedule_time,
            "payment_method": payment_method,
            "pro_member": pro_member,
            "status": "placed"
        }
        self.orders.append(order)
        return {"success": True, "data": {"order_id": len(self.orders), "platform": "foodpanda"}}

    def search_merchant_meituan(self, *, keyword, location, sort_by="comprehensive", filters=None, page=1, page_size=20):
        results = []
        for merchant in self.mock_merchants:
            if merchant["platform"] == "meituan" and keyword.lower() in merchant["name"].lower():
                results.append(merchant)
        start = (page - 1) * page_size
        end = start + page_size
        return {"success": True, "data": {"merchants": results[start:end], "total": len(results)}}

    def search_merchant_doordash(self, *, query, address, cuisine_type, price_range, dietary_preferences, rating_min, delivery_time_max, top_rated_only=False):
        results = []
        for merchant in self.mock_merchants:
            if merchant["platform"] == "doordash" and query.lower() in merchant["name"].lower():
                results.append(merchant)
        return {"success": True, "data": {"merchants": results, "total": len(results)}}

    def search_merchant_ubereats(self, *, search_term, delivery_location, price_level, dietary_restrictions, max_delivery_fee, max_delivery_time, sort_by="recommended"):
        results = []
        for merchant in self.mock_merchants:
            if merchant["platform"] == "ubereats" and search_term.lower() in merchant["name"].lower():
                results.append(merchant)
        return {"success": True, "data": {"merchants": results, "total": len(results)}}

    def search_merchant_foodpanda(self, *, search_text, area, cuisine, min_order_value, delivery_time, vouchers_only=False, free_delivery=False, page=1):
        results = []
        for merchant in self.mock_merchants:
            if merchant["platform"] == "foodpanda" and search_text.lower() in merchant["name"].lower():
                results.append(merchant)
        start = (page - 1) * 10
        end = start + 10
        return {"success": True, "data": {"merchants": results[start:end], "total": len(results)}}