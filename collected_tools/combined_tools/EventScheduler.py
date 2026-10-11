from BaseEnv import BaseEnv

class EventScheduler(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.users = self.parameters.get("users", [])
        self.events = self.parameters.get("events", [])
        self.sessions = self.parameters.get("sessions", [])
        self.blacklist = self.parameters.get("blacklist", [])

    def get_all_users(self):
        return {"success": True, "data": {"users": self.users}}

    def register_for_event(self, *, event_name, date, time):
        event_id = f"event_{len(self.events)+1}"
        event = {
            "id": event_id,
            "name": event_name,
            "date": date,
            "time": time,
            "participants": [],
            "blacklist": []
        }
        self.events.append(event)
        return {"success": True, "data": {"event_id": event_id}}

    def add_participant_details(self, *, event_id, user_id):
        for event in self.events:
            if event.get("id") == event_id:
                if user_id not in event.get("participants", []):
                    event["participants"].append(user_id)
                return {"success": True, "message": "Participant added."}
        return {"success": False, "message": "Event not found."}

    def list_events(self):
        return {"success": True, "data": {"events": self.events}}

    def edit_event(self, *, title, new_time):
        for event in self.events:
            if event.get("name") == title:
                event["time"] = new_time
                return {"success": True, "message": "Event updated."}
        return {"success": False, "message": "Event not found."}

    def send_notifications(self, *, title):
        for event in self.events:
            if event.get("name") == title:
                return {"success": True, "message": "Notifications sent to attendees."}
        return {"success": False, "message": "Event not found."}

    def list_sessions(self):
        return {"success": True, "data": {"sessions": self.sessions}}

    def delete_session(self, *, session_id):
        for session in self.sessions:
            if session.get("id") == session_id:
                self.sessions.remove(session)
                return {"success": True, "message": "Session deleted."}
        return {"success": False, "message": "Session not found."}

    def update_session(self, *, session_id, new_time=None, new_location=None):
        for session in self.sessions:
            if session.get("id") == session_id:
                if new_time is not None:
                    session["time"] = new_time
                if new_location is not None:
                    session["location"] = new_location
                return {"success": True, "message": "Session updated."}
        return {"success": False, "message": "Session not found."}

    def delete_event(self, *, event_id):
        for event in self.events:
            if event.get("id") == event_id:
                self.events.remove(event)
                return {"success": True, "message": "Event deleted."}
        return {"success": False, "message": "Event not found."}

    def add_to_blacklist(self, *, group_name):
        if group_name not in self.blacklist:
            self.blacklist.append(group_name)
        return {"success": True, "message": "Group added to blacklist."}