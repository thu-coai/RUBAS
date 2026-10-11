from BaseEnv import BaseEnv

class EmergencyDispatchSystem(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.incidents = self.parameters.get("incidents", [])
        self.resources = self.parameters.get("resources", [])
        self._incident_id_counter = 1

    def create_dispatch_request(
        self,
        *,
        incident_location,
        resource_ids,
        incident_type,
        incident_severity,
        incident_description
    ):
        if not isinstance(resource_ids, list):
            return {"success": False, "message": "resource_ids must be a list."}
        if incident_type not in ["Fire", "Medical", "Police"]:
            return {"success": False, "message": "Invalid incident_type."}
        if incident_severity not in ["Low", "Medium", "High"]:
            return {"success": False, "message": "Invalid incident_severity."}
        incident_id = f"INC{self._incident_id_counter}"
        self._incident_id_counter += 1
        incident = {
            "incident_id": incident_id,
            "incident_location": incident_location,
            "resource_ids": resource_ids,
            "incident_type": incident_type,
            "incident_severity": incident_severity,
            "incident_description": incident_description,
            "incident_status": "Active"
        }
        self.incidents.append(incident)
        return {"success": True, "data": {"incident_id": incident_id}}

    def redirect_dispatch_resources(
        self,
        *,
        resource_ids,
        target_type,
        incident_id_or_new_location
    ):
        if not isinstance(resource_ids, list):
            return {"success": False, "message": "resource_ids must be a list."}
        if target_type not in ["Incident", "Location"]:
            return {"success": False, "message": "Invalid target_type."}
        if target_type == "Incident":
            found = False
            for incident in self.incidents:
                if incident.get("incident_id") == incident_id_or_new_location:
                    incident["resource_ids"].extend(resource_ids)
                    found = True
                    break
            if not found:
                return {"success": False, "message": "Incident not found."}
            return {"success": True, "message": "Resources redirected to incident."}
        else:
            # Create new incident for the location
            incident_id = f"INC{self._incident_id_counter}"
            self._incident_id_counter += 1
            incident = {
                "incident_id": incident_id,
                "incident_location": incident_id_or_new_location,
                "resource_ids": resource_ids,
                "incident_type": "Unknown",
                "incident_severity": "Low",
                "incident_description": "Redirected resources to new location.",
                "incident_status": "Active"
            }
            self.incidents.append(incident)
            return {"success": True, "data": {"incident_id": incident_id}}

    def EstimateDispatchTime(
        self,
        *,
        resource_id,
        destination_location
    ):
        found = False
        for resource in self.resources:
            if resource.get("resource_id") == resource_id:
                found = True
                break
        if not found:
            return {"success": False, "message": "Resource not found."}
        # Simulate dispatch time (mock)
        dispatch_time_minutes = 10
        return {
            "success": True,
            "data": {
                "resource_id": resource_id,
                "destination_location": destination_location,
                "estimated_dispatch_time_minutes": dispatch_time_minutes
            }
        }

    def find_nearby_resources(
        self,
        *,
        location,
        resource_type=None,
        max_results=10
    ):
        results = []
        for resource in self.resources:
            if resource_type and resource.get("resource_type") != resource_type:
                continue
            results.append(resource)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"resources": results}}

    def get_incident_data(
        self,
        *,
        incident_id
    ):
        for incident in self.incidents:
            if incident.get("incident_id") == incident_id:
                return {"success": True, "data": incident}
        return {"success": False, "message": "Incident not found."}

    def get_resource_data(
        self,
        *,
        resource_id
    ):
        for resource in self.resources:
            if resource.get("resource_id") == resource_id:
                return {"success": True, "data": resource}
        return {"success": False, "message": "Resource not found."}

    def edit_incident(
        self,
        *,
        incident_id,
        incident_type=None,
        incident_severity=None,
        incident_description=None,
        incident_status=None,
        resource_ids=None
    ):
        for incident in self.incidents:
            if incident.get("incident_id") == incident_id:
                if incident_type is not None:
                    if incident_type in ["Fire", "Medical", "Police"]:
                        incident["incident_type"] = incident_type
                if incident_severity is not None:
                    if incident_severity in ["Low", "Medium", "High"]:
                        incident["incident_severity"] = incident_severity
                if incident_description is not None:
                    incident["incident_description"] = incident_description
                if incident_status is not None:
                    if incident_status in ["Active", "Closed"]:
                        incident["incident_status"] = incident_status
                if resource_ids is not None and isinstance(resource_ids, list):
                    incident["resource_ids"] = resource_ids
                return {"success": True, "message": "Incident updated."}
        return {"success": False, "message": "Incident not found."}

    def search_incidents(
        self,
        *,
        location,
        incident_type=None,
        severity=None,
        incident_status=None,
        max_results=10
    ):
        results = []
        for incident in self.incidents:
            if location and incident.get("incident_location") != location:
                continue
            if incident_type and incident.get("incident_type") != incident_type:
                continue
            if severity and incident.get("incident_severity") != severity:
                continue
            if incident_status and incident.get("incident_status") != incident_status:
                continue
            results.append(incident)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"incidents": results}}