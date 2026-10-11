from BaseEnv import BaseEnv

class Map(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.current_location = self.parameters.get("current_location", "123 Main St, Springfield, 12345")
        self.locations = self.parameters.get("locations", [
            {
                "address": "123 Main St, Springfield, 12345",
                "name": "Springfield Library",
                "open_now": True,
                "rating": 4.5,
                "coordinates": "39.799,-89.644",
                "reviews": [
                    {"user": "Alice", "rating": 5, "comment": "Great place!"},
                    {"user": "Bob", "rating": 4, "comment": "Nice and quiet."}
                ]
            },
            {
                "address": "456 Elm St, Springfield, 12345",
                "name": "Elm Cafe",
                "open_now": False,
                "rating": 4.0,
                "coordinates": "39.800,-89.650",
                "reviews": [
                    {"user": "Charlie", "rating": 4, "comment": "Good coffee."}
                ]
            }
        ])
        self.address_book = self.parameters.get("address_book", [])

    def get_current_location(self):
        return {"success": True, "data": {"current_location": self.current_location}}

    def search_locations(self, *, keywords, open_now=None, min_rating=None, base_location_address=None, max_distance=None, max_results=None):
        results = []
        for loc in self.locations:
            if keywords.lower() in loc.get("name", "").lower() or keywords.lower() in loc.get("address", "").lower():
                if open_now is not None and loc.get("open_now") != open_now:
                    continue
                if min_rating is not None and loc.get("rating", 0) < min_rating:
                    continue
                # Simulate distance filtering (mock: always include)
                results.append(loc)
        if max_results is not None:
            results = results[:max_results]
        return {"success": True, "data": {"locations": results}}

    def get_location_details(self, *, location_address):
        for loc in self.locations:
            if loc.get("address") == location_address:
                return {"success": True, "data": {"details": loc}}
        return {"success": False, "message": "Location not found."}

    def get_directions(self, *, start_location_address=None, end_location, mode):
        if mode not in ["driving", "walking", "transit"]:
            return {"success": False, "message": "Invalid mode of transportation."}
        # Simulate directions
        directions = {
            "start": start_location_address if start_location_address else self.current_location,
            "end": end_location,
            "mode": mode,
            "steps": [
                "Head north on Main St.",
                "Turn right onto Elm St.",
                "Arrive at destination."
            ]
        }
        return {"success": True, "data": {"directions": directions}}

    def geocoding(self, *, location_address):
        for loc in self.locations:
            if loc.get("address") == location_address:
                return {"success": True, "data": {"coordinates": loc.get("coordinates")}}
        # Simulate unknown address
        return {"success": True, "data": {"coordinates": "0.000,0.000"}}

    def reverse_geocoding(self, *, coordinates):
        for loc in self.locations:
            if loc.get("coordinates") == coordinates:
                return {"success": True, "data": {"address": loc.get("address")}}
        return {"success": True, "data": {"address": "Unknown address"}}

    def get_location_reviews(self, *, location_address):
        for loc in self.locations:
            if loc.get("address") == location_address:
                return {"success": True, "data": {"reviews": loc.get("reviews", [])}}
        return {"success": False, "message": "Location not found."}

    def search_address_book(self, *, keywords):
        results = []
        for entry in self.address_book:
            if keywords.lower() in entry.get("name", "").lower() or keywords.lower() in entry.get("address", "").lower():
                results.append(entry)
        return {"success": True, "data": {"address_book": results}}

    def add_address(self, *, name, address, note):
        entry = {"name": name, "address": address, "note": note}
        self.address_book.append(entry)
        return {"success": True, "message": "Address added to address book."}