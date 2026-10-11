from BaseEnv import BaseEnv

class Shipping(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.quotes = []
        self.shipments = []
        self.saved_addresses = self.parameters.get("saved_addresses", [])
        self.travel_agents = self.parameters.get("travel_agents", [])
        self.quote_counter = 1
        self.shipment_counter = 1

    def get_quote(self, *, package_details, sender_information, recipient_information, pickup_time, special_handling=None):
        if not isinstance(package_details, dict) or not isinstance(sender_information, dict) or not isinstance(recipient_information, dict):
            return {"success": False, "message": "Invalid input types for package_details, sender_information, or recipient_information."}
        for field in ["description", "weight", "dimensions"]:
            if field not in package_details:
                return {"success": False, "message": f"Missing {field} in package_details."}
        for field in ["full_name", "address", "contact_number"]:
            if field not in sender_information:
                return {"success": False, "message": f"Missing {field} in sender_information."}
            if field not in recipient_information:
                return {"success": False, "message": f"Missing {field} in recipient_information."}
        if not isinstance(pickup_time, str):
            return {"success": False, "message": "pickup_time must be a string."}
        quote_id = f"Q{self.quote_counter}"
        self.quote_counter += 1
        quote = {
            "quote_id": quote_id,
            "package_details": package_details,
            "sender_information": sender_information,
            "recipient_information": recipient_information,
            "pickup_time": pickup_time,
            "special_handling": special_handling if special_handling is not None else [],
            "price": 10.0 + 0.01 * package_details.get("weight", 0)
        }
        self.quotes.append(quote)
        return {"success": True, "data": {"quote_id": quote_id, "price": quote["price"]}}

    def create_shipment_label(self, *, quote_id, shipping_method):
        quote = next((q for q in self.quotes if q["quote_id"] == quote_id), None)
        if not quote:
            return {"success": False, "message": "Quote not found."}
        if shipping_method not in ["ground", "express", "overnight", "2-day"]:
            return {"success": False, "message": "Invalid shipping method."}
        shipment_id = f"S{self.shipment_counter}"
        self.shipment_counter += 1
        shipment = {
            "shipment_id": shipment_id,
            "quote_id": quote_id,
            "shipping_method": shipping_method,
            "status": "label_created",
            "details": quote,
            "estimated_delivery": "2024-12-31"
        }
        self.shipments.append(shipment)
        return {"success": True, "data": {"shipment_id": shipment_id, "label": f"Label for {shipment_id}"}}

    def get_shipment_details(self, *, shipment_id):
        shipment = next((s for s in self.shipments if s["shipment_id"] == shipment_id), None)
        if not shipment:
            return {"success": False, "message": "Shipment not found."}
        return {
            "success": True,
            "data": {
                "shipment_id": shipment_id,
                "status": shipment.get("status", "unknown"),
                "estimated_delivery": shipment.get("estimated_delivery", "unknown"),
                "details": shipment.get("details", {})
            }
        }

    def manage_shipment(self, *, shipment_id, operation, new_receipient_information=None, new_pickup_time=None):
        shipment = next((s for s in self.shipments if s["shipment_id"] == shipment_id), None)
        if not shipment:
            return {"success": False, "message": "Shipment not found."}
        if operation not in ["cancel", "reschedule_pickup", "redirect", "return_to_sender"]:
            return {"success": False, "message": "Invalid operation."}
        if operation == "cancel":
            shipment["status"] = "cancelled"
            return {"success": True, "message": "Shipment cancelled."}
        elif operation == "reschedule_pickup":
            if not new_pickup_time:
                return {"success": False, "message": "Missing new_pickup_time for reschedule_pickup."}
            shipment["details"]["pickup_time"] = new_pickup_time
            shipment["status"] = "pickup_rescheduled"
            return {"success": True, "message": "Pickup rescheduled."}
        elif operation == "redirect":
            if not new_receipient_information or not isinstance(new_receipient_information, dict):
                return {"success": False, "message": "Missing or invalid new_receipient_information for redirect."}
            shipment["details"]["recipient_information"] = new_receipient_information
            shipment["status"] = "redirected"
            return {"success": True, "message": "Shipment redirected."}
        elif operation == "return_to_sender":
            shipment["status"] = "return_to_sender"
            return {"success": True, "message": "Shipment will be returned to sender."}
        return {"success": False, "message": "Unknown error."}

    def search_shipment(self, *, search_term):
        results = []
        for shipment in self.shipments:
            if search_term in shipment.get("shipment_id", "") or search_term in shipment.get("status", ""):
                results.append(shipment)
        return {"success": True, "data": {"shipments": results}}

    def search_saved_addresses(self, *, search_term):
        results = []
        for addr in self.saved_addresses:
            if any(search_term in str(addr.get(k, "")) for k in ["full_name", "address", "contact_number"]):
                results.append(addr)
        return {"success": True, "data": {"addresses": results}}

    def search_travel_agents(self, *, search_text):
        results = []
        for agent in self.travel_agents:
            if search_text in agent.get("name", "") or search_text in agent.get("contact", ""):
                results.append(agent)
        return {"success": True, "data": {"travel_agents": results}}

    def ship_passport(self, *, receiver_name, receiver_address):
        shipment_id = f"S{self.shipment_counter}"
        self.shipment_counter += 1
        shipment = {
            "shipment_id": shipment_id,
            "item": "passport",
            "receiver_name": receiver_name,
            "receiver_address": receiver_address,
            "status": "in_transit"
        }
        self.shipments.append(shipment)
        return {"success": True, "data": {"shipment_id": shipment_id, "status": "in_transit"}}

    def search_shipping_quotes(self):
        return {"success": True, "data": {"quotes": self.quotes}}