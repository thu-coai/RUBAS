from BaseEnv import BaseEnv

class Ecommerce(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.orders = self.parameters.get("orders", [])
        self.products = self.parameters.get("products", [])

    def place_order_amazon(
        self,
        *,
        item_id,
        quantity,
        shipping_address,
        gift_message,
        shipping_method="standard",
        gift=False,
        prime=False
    ):
        if not isinstance(item_id, str) or not isinstance(quantity, int) or not isinstance(shipping_address, str) or not isinstance(gift_message, str):
            return {"success": False, "message": "Invalid argument types."}
        if shipping_method not in ["standard", "expedited", "prime"]:
            return {"success": False, "message": "Invalid shipping_method."}
        order = {
            "platform": "amazon",
            "item_id": item_id,
            "quantity": quantity,
            "shipping_address": shipping_address,
            "shipping_method": shipping_method,
            "gift": gift,
            "gift_message": gift_message,
            "prime": prime
        }
        self.orders.append(order)
        return {"success": True, "data": {"order": order}}

    def place_order_temu(
        self,
        *,
        item_id,
        quantity,
        shipping_address,
        color,
        size,
        insurance=False
    ):
        if not isinstance(item_id, str) or not isinstance(quantity, int) or not isinstance(shipping_address, str) or not isinstance(color, str) or not isinstance(size, str):
            return {"success": False, "message": "Invalid argument types."}
        order = {
            "platform": "temu",
            "item_id": item_id,
            "quantity": quantity,
            "shipping_address": shipping_address,
            "color": color,
            "size": size,
            "insurance": insurance
        }
        self.orders.append(order)
        return {"success": True, "data": {"order": order}}

    def place_order_ebay(
        self,
        *,
        item_id,
        quantity,
        shipping_address,
        offer_price,
        shipping_option="standard",
        payment_method="paypal"
    ):
        if not isinstance(item_id, str) or not isinstance(quantity, int) or not isinstance(shipping_address, str):
            return {"success": False, "message": "Invalid argument types."}
        if not isinstance(offer_price, (int, float)):
            return {"success": False, "message": "offer_price must be a number."}
        if shipping_option not in ["standard", "expedited"]:
            return {"success": False, "message": "Invalid shipping_option."}
        if payment_method not in ["paypal", "card"]:
            return {"success": False, "message": "Invalid payment_method."}
        order = {
            "platform": "ebay",
            "item_id": item_id,
            "quantity": quantity,
            "shipping_address": shipping_address,
            "offer_price": offer_price,
            "shipping_option": shipping_option,
            "payment_method": payment_method
        }
        self.orders.append(order)
        return {"success": True, "data": {"order": order}}

    def place_order_taobao(
        self,
        *,
        item_id,
        quantity,
        shipping_address,
        color_size,
        message_to_seller,
        delivery_option="standard",
        use_points=False
    ):
        if not isinstance(item_id, str) or not isinstance(quantity, int) or not isinstance(shipping_address, str) or not isinstance(color_size, str) or not isinstance(message_to_seller, str):
            return {"success": False, "message": "Invalid argument types."}
        if delivery_option not in ["standard", "express"]:
            return {"success": False, "message": "Invalid delivery_option."}
        order = {
            "platform": "taobao",
            "item_id": item_id,
            "quantity": quantity,
            "shipping_address": shipping_address,
            "color_size": color_size,
            "delivery_option": delivery_option,
            "message_to_seller": message_to_seller,
            "use_points": use_points
        }
        self.orders.append(order)
        return {"success": True, "data": {"order": order}}

    def search_products_amazon(
        self,
        *,
        keyword,
        category,
        min_rating,
        price_range,
        prime_only=False,
        sort_by="relevance",
        filters=None,
        page=1,
        page_size=20
    ):
        if not isinstance(keyword, str) or not isinstance(category, str):
            return {"success": False, "message": "Invalid argument types."}
        if not isinstance(min_rating, (int, float)) or not (1 <= min_rating <= 5):
            return {"success": False, "message": "min_rating must be between 1 and 5."}
        if not isinstance(price_range, list) or len(price_range) != 2:
            return {"success": False, "message": "price_range must be a list of two numbers."}
        if sort_by not in ["relevance", "price_asc", "price_desc", "rating", "reviews"]:
            return {"success": False, "message": "Invalid sort_by."}
        # Simulate search
        mock_products = [
            {
                "id": "A1",
                "name": f"{keyword} Product 1",
                "category": category,
                "rating": min_rating,
                "price": price_range[0],
                "prime": prime_only
            }
        ]
        return {"success": True, "data": {"products": mock_products}}

    def search_products_temu(
        self,
        *,
        query,
        category_id,
        min_price,
        max_price,
        sort_by="recommended",
        shipping_region="US",
        free_shipping=False,
        page=1
    ):
        if not isinstance(query, str) or not isinstance(category_id, str):
            return {"success": False, "message": "Invalid argument types."}
        if not isinstance(min_price, (int, float)) or not isinstance(max_price, (int, float)):
            return {"success": False, "message": "min_price and max_price must be numbers."}
        if sort_by not in ["recommended", "price_low", "price_high", "orders", "newest"]:
            return {"success": False, "message": "Invalid sort_by."}
        mock_products = [
            {
                "id": "T1",
                "name": f"{query} Product 1",
                "category_id": category_id,
                "price": min_price,
                "shipping_region": shipping_region,
                "free_shipping": free_shipping
            }
        ]
        return {"success": True, "data": {"products": mock_products}}

    def search_products_ebay(
        self,
        *,
        search_term,
        category,
        condition,
        min_price,
        max_price,
        buy_format,
        location,
        free_shipping=False,
        best_offer=False,
        returns_accepted=False,
        page_number=1
    ):
        if not isinstance(search_term, str) or not isinstance(category, str) or not isinstance(location, str):
            return {"success": False, "message": "Invalid argument types."}
        if not isinstance(condition, list) or not all(isinstance(c, str) for c in condition):
            return {"success": False, "message": "condition must be a list of strings."}
        if not isinstance(buy_format, list) or not all(isinstance(b, str) for b in buy_format):
            return {"success": False, "message": "buy_format must be a list of strings."}
        if not isinstance(min_price, (int, float)) or not isinstance(max_price, (int, float)):
            return {"success": False, "message": "min_price and max_price must be numbers."}
        mock_products = [
            {
                "id": "E1",
                "name": f"{search_term} Product 1",
                "category": category,
                "condition": condition,
                "price": min_price,
                "buy_format": buy_format,
                "location": location
            }
        ]
        return {"success": True, "data": {"products": mock_products}}

    def search_products_taobao(
        self,
        *,
        keyword,
        cat,
        price_range,
        location,
        delivery_time,
        sort="default",
        tmall_only=False,
        has_coupon=False,
        page=1,
        page_size=20
    ):
        if not isinstance(keyword, str) or not isinstance(cat, str) or not isinstance(location, str):
            return {"success": False, "message": "Invalid argument types."}
        if not isinstance(price_range, list) or len(price_range) != 2:
            return {"success": False, "message": "price_range must be a list of two numbers."}
        if not isinstance(delivery_time, int) or delivery_time < 1:
            return {"success": False, "message": "delivery_time must be an integer >= 1."}
        if sort not in ["default", "sales", "price_asc", "price_desc", "credit"]:
            return {"success": False, "message": "Invalid sort."}
        mock_products = [
            {
                "id": "TB1",
                "name": f"{keyword} Product 1",
                "cat": cat,
                "price": price_range[0],
                "location": location,
                "delivery_time": delivery_time
            }
        ]
        return {"success": True, "data": {"products": mock_products}}