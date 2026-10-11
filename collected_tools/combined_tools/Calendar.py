from BaseEnv import BaseEnv

class Calendar(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.events = self.parameters.get("events", [])

    def get_day_calendar_events(self, *, date, name=None):
        if not isinstance(date, str):
            return {"success": False, "message": "Invalid date format."}
        filtered = []
        for event in self.events:
            if event.get("date") == date:
                if name is None or event.get("name") == name:
                    filtered.append(event)
        return {"success": True, "data": {"events": filtered}}

    def create_calendar_event(self, *, date, name, event, start_time=None, end_time=None, attendees=None):
        if not isinstance(date, str) or not isinstance(name, str) or not isinstance(event, str):
            return {"success": False, "message": "Invalid input types for required fields."}
        new_event = {
            "date": date,
            "name": name,
            "event": event,
            "start_time": start_time,
            "end_time": end_time,
            "attendees": attendees if attendees is not None else []
        }
        self.events.append(new_event)
        return {"success": True, "message": "Event created successfully."}

    def cancel_calendar_event(self, *, date, name, event):
        if not isinstance(date, str) or not isinstance(name, str) or not isinstance(event, str):
            return {"success": False, "message": "Invalid input types for required fields."}
        removed = False
        for e in list(self.events):
            if e.get("date") == date and e.get("name") == name and e.get("event") == event:
                self.events.remove(e)
                removed = True
                break
        if removed:
            return {"success": True, "message": "Event cancelled successfully."}
        else:
            return {"success": False, "message": "Event not found."}

    def reschedule_calendar_event(self, *, name, event, reschedule_date):
        if not isinstance(name, str) or not isinstance(event, str) or not isinstance(reschedule_date, str):
            return {"success": False, "message": "Invalid input types for required fields."}
        found = False
        for e in self.events:
            if e.get("name") == name and e.get("event") == event:
                e["date"] = reschedule_date
                found = True
                break
        if found:
            return {"success": True, "message": "Event rescheduled successfully."}
        else:
            return {"success": False, "message": "Event not found."}