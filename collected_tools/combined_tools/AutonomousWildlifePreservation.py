from BaseEnv import BaseEnv

class AutonomousWildlifePreservation(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.blog_updates = self.parameters.get("blog_updates", [])
        self.population_data_sources = self.parameters.get("population_data_sources", {})
        self.notifications = self.parameters.get("notifications", [])
        self.weather_data = self.parameters.get("weather_data", {"forecast": "Sunny"})
        self.food_supplies = self.parameters.get("food_supplies", {})
        self.food_requirements = self.parameters.get("food_requirements", {})
        self.environmental_controls = self.parameters.get("environmental_controls", {})
        self.animal_habitats = self.parameters.get("animal_habitats", [])

    def post_update(self, *, content):
        if not isinstance(content, str) or not content.strip():
            return {"success": False, "message": "Content must be a non-empty string."}
        self.blog_updates.append({"content": content})
        return {"success": True, "message": "Update posted to the conservation blog."}

    def get_population_data(self, *, source):
        if not isinstance(source, str) or not source.strip():
            return {"success": False, "message": "Source must be a non-empty string."}
        data = self.population_data_sources.get(source, {"population": "unknown"})
        return {"success": True, "data": {"source": source, "population_data": data}}

    def deactivate_notification(self, *, notification_id):
        if not isinstance(notification_id, str) or not notification_id.strip():
            return {"success": False, "message": "notification_id must be a non-empty string."}
        found = False
        for n in self.notifications:
            if n.get("id") == notification_id:
                n["active"] = False
                found = True
                break
        if found:
            return {"success": True, "message": f"Notification {notification_id} deactivated."}
        else:
            return {"success": False, "message": f"Notification {notification_id} not found."}

    def list_urgent_notifications(self):
        urgent = [n for n in self.notifications if n.get("urgent", False) and n.get("active", True)]
        return {"success": True, "data": {"urgent_notifications": urgent}}

    def access_weather_data(self):
        return {"success": True, "data": {"weather": self.weather_data}}

    def update_food_supplies(self, *, animal_type, quantity):
        if not isinstance(animal_type, str) or not animal_type.strip():
            return {"success": False, "message": "animal_type must be a non-empty string."}
        if not isinstance(quantity, str) or not quantity.strip():
            return {"success": False, "message": "quantity must be a non-empty string."}
        self.food_supplies[animal_type] = quantity
        return {"success": True, "message": f"Food supplies for {animal_type} updated to {quantity}."}

    def modify_environmental_controls(self, *, zone, control, value):
        if not all(isinstance(x, str) and x.strip() for x in [zone, control, value]):
            return {"success": False, "message": "zone, control, and value must be non-empty strings."}
        if zone not in self.environmental_controls:
            self.environmental_controls[zone] = {}
        self.environmental_controls[zone][control] = value
        return {"success": True, "message": f"Set {control} in zone {zone} to {value}."}

    def get_food_supplies(self):
        return {"success": True, "data": {"food_supplies": self.food_supplies}}

    def get_food_requirements(self):
        return {"success": True, "data": {"food_requirements": self.food_requirements}}

    def list_animal_habitats(self):
        return {"success": True, "data": {"animal_habitats": self.animal_habitats}}