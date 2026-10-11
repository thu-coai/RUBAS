from BaseEnv import BaseEnv

class HomeAssistant(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.door_locked = True
        self.guests = self.parameters.get("guests", [])
        self.guest_id_counter = 1
        self.access_history = self.parameters.get("access_history", [])
        self.access_list = self.parameters.get("access_list", [])
        self.devices = self.parameters.get("devices", [
            {"name": "Living Room Light", "status": "on"},
            {"name": "Thermostat", "status": "on"},
            {"name": "Security Camera", "status": "on"}
        ])
        self.objects = self.parameters.get("objects", [
            {"name": "Safe", "allowed_operations": ["open", "close"]},
            {"name": "Garage Door", "allowed_operations": ["open", "close"]}
        ])
        self.operations = self.parameters.get("operations", [
            {"id": "op1", "object": "Safe", "operation": "open"},
            {"id": "op2", "object": "Garage Door", "operation": "close"}
        ])
        self.reminders = self.parameters.get("reminders", [])
        self.alarm_active = False
        self.owner_contacted = False

    def unlock_door(self):
        if not self.door_locked:
            return {"success": True, "message": "Door is already unlocked."}
        self.door_locked = False
        self.access_history.append({"action": "unlock_door"})
        return {"success": True, "message": "Door unlocked."}

    def add_guest(self, *, guest_name, guest_email):
        guest_id = f"guest{self.guest_id_counter}"
        self.guest_id_counter += 1
        guest = {"id": guest_id, "name": guest_name, "email": guest_email}
        self.guests.append(guest)
        return {"success": True, "data": {"guest": guest}}

    def delete_guest(self, *, guest_ids):
        removed = []
        for gid in guest_ids:
            for guest in self.guests:
                if guest.get("id") == gid:
                    self.guests.remove(guest)
                    removed.append(gid)
                    break
        return {"success": True, "data": {"removed_guest_ids": removed}}

    def check_lock_status(self):
        status = "locked" if self.door_locked else "unlocked"
        return {"success": True, "data": {"lock_status": status}}

    def view_access_history(self, *, start_time=None, end_time=None):
        # For simulation, ignore time filtering
        return {"success": True, "data": {"access_history": self.access_history}}

    def grant_access(self, *, name, period, permanent, email=None):
        access = {
            "name": name,
            "period": period,
            "permanent": permanent,
            "email": email
        }
        self.access_list.append(access)
        self.access_history.append({"action": "grant_access", "name": name})
        return {"success": True, "data": {"access": access}}

    def remove_access(self, *, name, email=None):
        removed = []
        for access in list(self.access_list):
            if access.get("name") == name and (email is None or access.get("email") == email):
                self.access_list.remove(access)
                removed.append(access)
        self.access_history.append({"action": "remove_access", "name": name})
        return {"success": True, "data": {"removed": removed}}

    def search_guests(self, *, search_text):
        res = []
        for guest in self.guests:
            if search_text.lower() in guest.get("name", "").lower() or search_text.lower() in guest.get("email", "").lower():
                res.append(guest)
        return {"success": True, "data": {"guests": res}}

    def search_devices(self, *, search_text=None):
        if not search_text:
            return {"success": True, "data": {"devices": self.devices}}
        res = []
        for device in self.devices:
            if search_text.lower() in device.get("name", "").lower():
                res.append(device)
        return {"success": True, "data": {"devices": res}}

    def turn_off_devices(self, *, names):
        turned_off = []
        for device in self.devices:
            if device["name"] in names:
                device["status"] = "off"
                turned_off.append(device["name"])
        return {"success": True, "data": {"turned_off": turned_off}}

    def get_all_objects(self):
        return {"success": True, "data": {"objects": self.objects}}

    def search_objects(self, *, search_text=None):
        if not search_text:
            return {"success": True, "data": {"objects": self.objects}}
        res = []
        for obj in self.objects:
            if search_text.lower() in obj.get("name", "").lower():
                res.append(obj)
        return {"success": True, "data": {"objects": res}}

    def get_allowed_operations(self, *, name):
        for obj in self.objects:
            if obj.get("name") == name:
                return {"success": True, "data": {"allowed_operations": obj.get("allowed_operations", [])}}
        return {"success": False, "message": "Object not found."}

    def perform_operation(self, *, id):
        for op in self.operations:
            if op.get("id") == id:
                return {"success": True, "message": f"Operation {op['operation']} on {op['object']} performed."}
        return {"success": False, "message": "Operation not found."}

    def activate_alarm(self):
        self.alarm_active = True
        self.access_history.append({"action": "activate_alarm"})
        return {"success": True, "message": "Alarm activated."}

    def contact_owner(self):
        self.owner_contacted = True
        self.access_history.append({"action": "contact_owner"})
        return {"success": True, "message": "Owner contacted."}

    def set_reminder(self, *, reminder_text, date_time):
        reminder = {"reminder_text": reminder_text, "date_time": date_time}
        self.reminders.append(reminder)
        return {"success": True, "data": {"reminder": reminder}}

    def query_aid_impact(self, *, region):
        # Simulate a mock response
        info = {
            "region": region,
            "impact": "Aid has reached 80% of the population.",
            "challenges": "Logistical difficulties due to ongoing conflict."
        }
        return {"success": True, "data": info}