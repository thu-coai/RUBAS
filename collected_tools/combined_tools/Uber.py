from BaseEnv import BaseEnv

class Uber(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.rides = self.parameters.get("rides", [])
        self.ride_id_counter = 1
        self.ride_history = self.parameters.get("ride_history", [])
        self.payments = self.parameters.get("payments", [])
        self.shared_locations = []
        self.ratings = []
        self.coupons = self.parameters.get("coupons", [])

    def request_ride(self, *, pickup_location, destination, ride_type):
        ride = {
            "ride_id": f"ride_{self.ride_id_counter}",
            "pickup_location": pickup_location,
            "destination": destination,
            "ride_type": ride_type,
            "status": "requested"
        }
        self.rides.append(ride)
        self.ride_history.append(ride)
        self.ride_id_counter += 1
        return {
            "success": True,
            "data": {"ride_id": ride["ride_id"], "status": "requested"}
        }

    def view_ride_history(self, *, user_id, start_date, end_date):
        # Simulate filtering by returning all rides for simplicity
        rides = [ride for ride in self.ride_history if ride.get("user_id", user_id) == user_id]
        return {
            "success": True,
            "data": {"rides": rides}
        }

    def pay_ride_fare(self, *, ride_id, payment_method, amount):
        payment = {
            "ride_id": ride_id,
            "payment_method": payment_method,
            "amount": amount,
            "status": "paid"
        }
        self.payments.append(payment)
        return {
            "success": True,
            "data": {"ride_id": ride_id, "status": "paid"}
        }

    def share_location(self, *, recipient_id, location):
        entry = {
            "recipient_id": recipient_id,
            "location": location
        }
        self.shared_locations.append(entry)
        return {
            "success": True,
            "message": f"Location shared with {recipient_id}."
        }

    def rate_driver(self, *, ride_id, rating, feedback=None):
        if not (1 <= rating <= 5):
            return {
                "success": False,
                "message": "Rating must be between 1 and 5."
            }
        entry = {
            "ride_id": ride_id,
            "rating": rating,
            "feedback": feedback
        }
        self.ratings.append(entry)
        return {
            "success": True,
            "message": "Driver rated successfully."
        }

    def view_coupons(self, *, user_id, coupon_code=None):
        user_coupons = [c for c in self.coupons if c.get("user_id") == user_id]
        if coupon_code:
            filtered = [c for c in user_coupons if c.get("code") == coupon_code]
            return {
                "success": True,
                "data": {"coupons": filtered}
            }
        return {
            "success": True,
            "data": {"coupons": user_coupons}
        }