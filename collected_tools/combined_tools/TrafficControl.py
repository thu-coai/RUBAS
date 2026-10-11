from BaseEnv import BaseEnv

class TrafficControl(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.roads = self.parameters.get("roads", [
            {"id": "road1", "name": "Main St", "details": {"lanes": 2, "speed_limit": 40}},
            {"id": "road2", "name": "Broadway", "details": {"lanes": 3, "speed_limit": 35}}
        ])
        self.intersections = self.parameters.get("intersections", [
            {"id": "int1", "name": "Main & 1st", "details": {"roads": ["road1", "road2"]}},
            {"id": "int2", "name": "Broadway & 2nd", "details": {"roads": ["road2"]}}
        ])
        self.traffic_lights = self.parameters.get("traffic_lights", {
            "int1": {
                "vehicle-north-south": "red",
                "vehicle-east-west": "green",
                "pedestrian-north-south": "walk",
                "pedestrian-east-west": "stop"
            },
            "int2": {
                "vehicle-north-south": "green",
                "vehicle-east-west": "red",
                "pedestrian-north-south": "stop",
                "pedestrian-east-west": "walk"
            }
        })
        self.maintenance_schedule = self.parameters.get("maintenance_schedule", [])
        self.priority_schedules = self.parameters.get("priority_schedules", [])
        self.traffic_congestion = self.parameters.get("traffic_congestion", {})
        self.traffic_patterns = self.parameters.get("traffic_patterns", {})

    def search_locations(self, *, location_name, location_type=None):
        results = []
        if location_type is None or location_type == "road":
            for road in self.roads:
                if location_name.lower() in road["name"].lower():
                    results.append({"type": "road", "id": road["id"], "name": road["name"]})
        if location_type is None or location_type == "intersection":
            for intersection in self.intersections:
                if location_name.lower() in intersection["name"].lower():
                    results.append({"type": "intersection", "id": intersection["id"], "name": intersection["name"]})
        return {"success": True, "data": {"locations": results}}

    def get_road_details(self, *, road_id):
        for road in self.roads:
            if road["id"] == road_id:
                return {"success": True, "data": {"road": road}}
        return {"success": False, "message": "Road not found."}

    def get_intersection_details(self, *, intersection_id):
        for intersection in self.intersections:
            if intersection["id"] == intersection_id:
                return {"success": True, "data": {"intersection": intersection}}
        return {"success": False, "message": "Intersection not found."}

    def search_route(self, *, origin_id, destination_id, max_results=1):
        # Simulate a route as a list of location ids
        if origin_id == destination_id:
            return {"success": True, "data": {"routes": [[origin_id]]}}
        route = [origin_id, destination_id]
        routes = [route for _ in range(max_results)]
        return {"success": True, "data": {"routes": routes}}

    def check_traffic_lights_states(self, *, intersection_id):
        states = self.traffic_lights.get(intersection_id)
        if states is None:
            return {"success": False, "message": "Intersection not found or no traffic lights."}
        return {"success": True, "data": {"traffic_lights": states}}

    def manage_traffic_light_state(self, *, intersection_id, traffic_light_id, traffic_light_state, start_time=None, end_time=None):
        if intersection_id not in self.traffic_lights:
            return {"success": False, "message": "Intersection not found."}
        self.traffic_lights[intersection_id][traffic_light_id] = traffic_light_state
        return {"success": True, "message": "Traffic light state updated."}

    def monitor_traffic_congestion(self, *, location_id):
        level = self.traffic_congestion.get(location_id, "moderate")
        return {"success": True, "data": {"congestion_level": level}}

    def predict_traffic_congestion(self, *, for_location_id=None, location_id=None, prediction_start_time=None, prediction_end_time=None):
        # Accept both for_location_id and location_id for robustness
        loc_id = location_id if location_id is not None else for_location_id
        prediction = {
            "location_id": loc_id,
            "start_time": prediction_start_time,
            "end_time": prediction_end_time,
            "predicted_congestion": "moderate"
        }
        return {"success": True, "data": prediction}

    def analyze_traffic_patterns(self, *, location_id, start_time, end_time):
        pattern = self.traffic_patterns.get(location_id, {"summary": "Normal traffic pattern."})
        return {"success": True, "data": {"location_id": location_id, "start_time": start_time, "end_time": end_time, "pattern": pattern}}

    def give_priority_to_emergency_vehicle(self, *, intersection_ids, start_time, end_time):
        self.priority_schedules.append({
            "type": "emergency_vehicle",
            "intersection_ids": intersection_ids,
            "start_time": start_time,
            "end_time": end_time
        })
        return {"success": True, "message": "Priority given to emergency vehicle."}

    def give_priority_to_public_transportation(self, *, intersection_ids, start_time, end_time):
        self.priority_schedules.append({
            "type": "public_transportation",
            "intersection_ids": intersection_ids,
            "start_time": start_time,
            "end_time": end_time
        })
        return {"success": True, "message": "Priority given to public transportation."}

    def schedule_road_maintenance(self, *, location_id, start_time, end_time):
        self.maintenance_schedule.append({
            "location_id": location_id,
            "start_time": start_time,
            "end_time": end_time
        })
        return {"success": True, "message": "Road maintenance scheduled."}