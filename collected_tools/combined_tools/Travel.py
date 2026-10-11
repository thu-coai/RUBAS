from BaseEnv import BaseEnv

class Travel(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.user_info = self.parameters.get("user_info", {
            "first_name": "John",
            "last_name": "Doe",
            "id_number": "123456789",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "address": "123 Main St, City",
            "passport_number": "A1234567",
            "bank_account_number": "987654321",
            "credit_card_number": "4111111111111111"
        })
        self.hotels = self.parameters.get("hotels", [
            {"id": "h1", "name": "Grand Hotel", "city": "Metropolis", "address": "1 Hotel Ave", "rating": 4.5, "reviews": ["Great stay!", "Clean rooms."]},
            {"id": "h2", "name": "Budget Inn", "city": "Metropolis", "address": "2 Cheap St", "rating": 3.8, "reviews": ["Affordable.", "Basic amenities."]}
        ])
        self.restaurants = self.parameters.get("restaurants", [
            {"name": "Steak House", "city": "Metropolis", "address": "10 Food Rd", "price_per_person": 30, "rating": 4.2, "reviews": ["Delicious steaks!", "Nice ambiance."], "contact": "+1234567891", "opening_hours": "10:00-22:00"},
            {"name": "Veggie Delight", "city": "Metropolis", "address": "11 Green St", "price_per_person": 20, "rating": 4.0, "reviews": ["Fresh veggies!", "Healthy options."], "contact": "+1234567892", "opening_hours": "09:00-21:00"}
        ])
        self.car_rentals = self.parameters.get("car_rentals", [
            {"name": "City Cars", "city": "Metropolis", "address": "20 Drive Ln", "price_per_day": 40, "rating": 4.1, "reviews": ["Easy pickup.", "Good cars."]},
            {"name": "Budget Wheels", "city": "Metropolis", "address": "21 Save Ave", "price_per_day": 30, "rating": 3.9, "reviews": ["Cheap rates.", "Older vehicles."]}
        ])
        self.hotel_reservations = []
        self.restaurant_reservations = []
        self.weather_forecast = self.parameters.get("weather_forecast", {
            "2024-07-01": "Sunny",
            "2024-07-02": "Cloudy"
        })
        self.flights = self.parameters.get("flights", [
            {"destination": "Metropolis", "flight_number": "MT123", "departure": "2024-07-01 09:00"},
            {"destination": "Metropolis", "flight_number": "MT456", "departure": "2024-07-01 15:00"}
        ])
        self.suggestions = self.parameters.get("suggestions", [
            "Visit the city museum.",
            "Try local cuisine.",
            "Book hotels in advance."
        ])
        self.travel_routes = self.parameters.get("travel_routes", [
            {"from": "Airport", "to": "Grand Hotel", "route": "Taxi, 20 min"},
            {"from": "Grand Hotel", "to": "Steak House", "route": "Walk, 5 min"}
        ])

    def get_user_information(self):
        return {"success": True, "data": self.user_info}

    def get_all_hotels_in_city(self, *, city):
        hotels_in_city = [h for h in self.hotels if h.get("city", "") == city]
        return {"success": True, "data": {"hotels": hotels_in_city}}

    def get_hotel_address(self, *, hotel_name):
        for h in self.hotels:
            if h.get("name", "") == hotel_name:
                return {"success": True, "data": {"address": h.get("address", "")}}
        return {"success": False, "message": "Hotel not found."}

    def get_all_restaurants_in_city(self, *, city):
        restaurants_in_city = [r for r in self.restaurants if r.get("city", "") == city]
        return {"success": True, "data": {"restaurants": restaurants_in_city}}

    def get_restaurant_address(self, *, restaurant_name):
        for r in self.restaurants:
            if r.get("name", "") == restaurant_name:
                return {"success": True, "data": {"address": r.get("address", "")}}
        return {"success": False, "message": "Restaurant not found."}

    def get_price_for_restaurants(self, *, restaurant_name):
        for r in self.restaurants:
            if r.get("name", "") == restaurant_name:
                return {"success": True, "data": {"price_per_person": r.get("price_per_person", None)}}
        return {"success": False, "message": "Restaurant not found."}

    def get_all_car_rental_companies_in_city(self, *, city):
        companies_in_city = [c for c in self.car_rentals if c.get("city", "") == city]
        return {"success": True, "data": {"car_rental_companies": companies_in_city}}

    def get_car_rental_address(self, *, company_name):
        for c in self.car_rentals:
            if c.get("name", "") == company_name:
                return {"success": True, "data": {"address": c.get("address", "")}}
        return {"success": False, "message": "Car rental company not found."}

    def reserve_hotel(self, *, hotel_name, reservation_time):
        for h in self.hotels:
            if h.get("name", "") == hotel_name:
                reservation = {"hotel_name": hotel_name, "reservation_time": reservation_time}
                self.hotel_reservations.append(reservation)
                return {"success": True, "data": {"reservation": reservation}}
        return {"success": False, "message": "Hotel not found."}

    def reserve_restaurant(self, *, restaurant_name, start_time):
        for r in self.restaurants:
            if r.get("name", "") == restaurant_name:
                reservation = {"restaurant_name": restaurant_name, "start_time": start_time}
                self.restaurant_reservations.append(reservation)
                return {"success": True, "data": {"reservation": reservation}}
        return {"success": False, "message": "Restaurant not found."}

    def get_rating_reviews_for_restaurant(self, *, restaurant_name):
        for r in self.restaurants:
            if r.get("name", "") == restaurant_name:
                return {"success": True, "data": {"rating": r.get("rating", None), "reviews": r.get("reviews", [])}}
        return {"success": False, "message": "Restaurant not found."}

    def get_contact_information_for_restaurants(self, *, restaurant_name):
        for r in self.restaurants:
            if r.get("name", "") == restaurant_name:
                return {"success": True, "data": {"contact": r.get("contact", "")}}
        return {"success": False, "message": "Restaurant not found."}

    def check_restaurant_opening_hours(self, *, restaurant_name):
        for r in self.restaurants:
            if r.get("name", "") == restaurant_name:
                return {"success": True, "data": {"opening_hours": r.get("opening_hours", "")}}
        return {"success": False, "message": "Restaurant not found."}

    def get_rating_reviews_for_car_rental(self, *, company_name):
        for c in self.car_rentals:
            if c.get("name", "") == company_name:
                return {"success": True, "data": {"rating": c.get("rating", None), "reviews": c.get("reviews", [])}}
        return {"success": False, "message": "Car rental company not found."}

    def get_car_price_per_day(self, *, company_name):
        for c in self.car_rentals:
            if c.get("name", "") == company_name:
                return {"success": True, "data": {"price_per_day": c.get("price_per_day", None)}}
        return {"success": False, "message": "Car rental company not found."}

    def get_rating_reviews_for_hotel(self, *, hotel_name):
        for h in self.hotels:
            if h.get("name", "") == hotel_name:
                return {"success": True, "data": {"rating": h.get("rating", None), "reviews": h.get("reviews", [])}}
        return {"success": False, "message": "Hotel not found."}

    def search_hotels(self, *, search_text=None):
        if not search_text:
            return {"success": True, "data": {"hotels": self.hotels}}
        res = [h for h in self.hotels if search_text.lower() in h.get("name", "").lower()]
        return {"success": True, "data": {"hotels": res}}

    def book_hotel(self, *, hotel_id, check_in_time, check_out_time, room_count):
        for h in self.hotels:
            if h.get("id", "") == hotel_id:
                booking = {
                    "hotel_id": hotel_id,
                    "check_in_time": check_in_time,
                    "check_out_time": check_out_time,
                    "room_count": room_count
                }
                self.hotel_reservations.append(booking)
                return {"success": True, "data": {"booking": booking}}
        return {"success": False, "message": "Hotel not found."}

    def get_travel_routes(self):
        return {"success": True, "data": {"routes": self.travel_routes}}

    def get_forecast(self, *, date):
        forecast = self.weather_forecast.get(date, "No forecast available.")
        return {"success": True, "data": {"date": date, "forecast": forecast}}

    def get_suggestions(self):
        return {"success": True, "data": {"suggestions": self.suggestions}}

    def search_flights(self, *, destination):
        flights = [f for f in self.flights if f.get("destination", "") == destination]
        return {"success": True, "data": {"flights": flights}}