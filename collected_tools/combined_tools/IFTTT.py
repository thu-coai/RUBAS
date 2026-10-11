from BaseEnv import BaseEnv

class IFTTT(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.connected_services = self.parameters.get("connected_services", [
            {"name": "Twitter"},
            {"name": "Gmail"},
            {"name": "Weather"},
            {"name": "Hue"}
        ])
        self.triggers = self.parameters.get("triggers", {
            "Twitter": [
                {"name": "new tweet from user", "description": "Triggered when a user tweets."},
                {"name": "new follower", "description": "Triggered when a user gets a new follower."}
            ],
            "Gmail": [
                {"name": "received email", "description": "Triggered when a new email is received."}
            ],
            "Weather": [
                {"name": "temperature drops", "description": "Triggered when temperature drops below a threshold."}
            ]
        })
        self.actions = self.parameters.get("actions", {
            "Twitter": [
                {"name": "post tweet", "description": "Post a tweet."}
            ],
            "Gmail": [
                {"name": "send email", "description": "Send an email."}
            ],
            "Hue": [
                {"name": "turn on light", "description": "Turn on a Hue light."}
            ]
        })
        self.applets = self.parameters.get("applets", [])
        self._applet_id_counter = 1

    def search_connected_services(self, *, keywords, max_results=5):
        if not isinstance(keywords, str):
            return {"success": False, "message": "keywords must be a string."}
        results = []
        for service in self.connected_services:
            if keywords.lower() in service["name"].lower():
                results.append(service)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"services": results}}

    def search_triggers(self, *, service_name, keywords, max_results=10):
        if not isinstance(service_name, str) or not isinstance(keywords, str):
            return {"success": False, "message": "service_name and keywords must be strings."}
        if not any(s["name"] == service_name for s in self.connected_services):
            return {"success": False, "message": f"Service {service_name} is not connected."}
        triggers = self.triggers.get(service_name, [])
        results = []
        for trig in triggers:
            if keywords.lower() in trig["name"].lower():
                results.append(trig)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"triggers": results}}

    def search_actions(self, *, service_name, keywords, max_results=10):
        if not isinstance(service_name, str) or not isinstance(keywords, str):
            return {"success": False, "message": "service_name and keywords must be strings."}
        if not any(s["name"] == service_name for s in self.connected_services):
            return {"success": False, "message": f"Service {service_name} is not connected."}
        actions = self.actions.get(service_name, [])
        results = []
        for act in actions:
            if keywords.lower() in act["name"].lower():
                results.append(act)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"actions": results}}

    def create_applet(self, *, trigger_service_name, trigger_name, trigger_parameters,
                      action_service_name, action_name, action_parameters):
        if not any(s["name"] == trigger_service_name for s in self.connected_services):
            return {"success": False, "message": f"Trigger service {trigger_service_name} is not connected."}
        if not any(s["name"] == action_service_name for s in self.connected_services):
            return {"success": False, "message": f"Action service {action_service_name} is not connected."}
        if not any(t["name"] == trigger_name for t in self.triggers.get(trigger_service_name, [])):
            return {"success": False, "message": f"Trigger {trigger_name} not found for service {trigger_service_name}."}
        if not any(a["name"] == action_name for a in self.actions.get(action_service_name, [])):
            return {"success": False, "message": f"Action {action_name} not found for service {action_service_name}."}
        applet_id = f"applet_{self._applet_id_counter}"
        self._applet_id_counter += 1
        applet = {
            "id": applet_id,
            "trigger_service_name": trigger_service_name,
            "trigger_name": trigger_name,
            "trigger_parameters": trigger_parameters,
            "action_service_name": action_service_name,
            "action_name": action_name,
            "action_parameters": action_parameters
        }
        self.applets.append(applet)
        return {"success": True, "data": {"applet_id": applet_id}}

    def search_applets(self, trigger_keywords=None, action_keywords=None, max_results=None):
        results = []
        for applet in self.applets:
            trigger_match = True
            action_match = True
            if trigger_keywords:
                trigger_match = trigger_keywords.lower() in applet["trigger_name"].lower()
            if action_keywords:
                action_match = action_keywords.lower() in applet["action_name"].lower()
            if trigger_match and action_match:
                results.append(applet)
            if max_results is not None and len(results) >= max_results:
                break
        return {"success": True, "data": {"applets": results}}

    def update_applet(self, *, applet_id, trigger_service_name, trigger_name, trigger_parameters,
                      action_service_name, action_name, action_parameters):
        applet = next((a for a in self.applets if a["id"] == applet_id), None)
        if not applet:
            return {"success": False, "message": f"Applet {applet_id} not found."}
        if not any(s["name"] == trigger_service_name for s in self.connected_services):
            return {"success": False, "message": f"Trigger service {trigger_service_name} is not connected."}
        if not any(s["name"] == action_service_name for s in self.connected_services):
            return {"success": False, "message": f"Action service {action_service_name} is not connected."}
        if not any(t["name"] == trigger_name for t in self.triggers.get(trigger_service_name, [])):
            return {"success": False, "message": f"Trigger {trigger_name} not found for service {trigger_service_name}."}
        if not any(a["name"] == action_name for a in self.actions.get(action_service_name, [])):
            return {"success": False, "message": f"Action {action_name} not found for service {action_service_name}."}
        applet.update({
            "trigger_service_name": trigger_service_name,
            "trigger_name": trigger_name,
            "trigger_parameters": trigger_parameters,
            "action_service_name": action_service_name,
            "action_name": action_name,
            "action_parameters": action_parameters
        })
        return {"success": True, "message": f"Applet {applet_id} updated."}

    def delete_applets(self, *, applet_ids):
        if not isinstance(applet_ids, list):
            return {"success": False, "message": "applet_ids must be a list."}
        deleted = []
        for applet_id in applet_ids:
            applet = next((a for a in self.applets if a["id"] == applet_id), None)
            if applet:
                self.applets.remove(applet)
                deleted.append(applet_id)
        return {"success": True, "data": {"deleted_applets": deleted}}