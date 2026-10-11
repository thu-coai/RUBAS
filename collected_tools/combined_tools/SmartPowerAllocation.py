from BaseEnv import BaseEnv

class SmartPowerAllocation(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.appliance_distribution = self.parameters.get("appliance_distribution", {})
        self.documents = self.parameters.get("documents", {})
        self.announcements = self.parameters.get("announcements", [])
        self.sector_power = self.parameters.get("sector_power", {})
        self.sections = self.parameters.get("sections", {})
        self.buildings = self.parameters.get("buildings", [])
        self.grids = self.parameters.get("grids", [])
        self.power_usage_data = self.parameters.get("power_usage_data", {})
        self.grid_status = self.parameters.get("grid_status", [])

    def get_current_distribution(self):
        return {
            "success": True,
            "data": {"appliance_distribution": self.appliance_distribution}
        }

    def update_power_distribution(self, *, appliance, start_time, end_time):
        if not isinstance(appliance, str) or not isinstance(start_time, str) or not isinstance(end_time, str):
            return {"success": False, "message": "Invalid input types."}
        self.appliance_distribution[appliance] = {
            "start_time": start_time,
            "end_time": end_time
        }
        return {"success": True, "message": f"Updated power distribution for {appliance}."}

    def read_document(self, *, document_name):
        if not isinstance(document_name, str):
            return {"success": False, "message": "Invalid document name."}
        content = self.documents.get(document_name, None)
        if content is None:
            return {"success": False, "message": "Document not found."}
        return {"success": True, "data": {"content": content}}

    def publish_announcement(self, *, announcement_content):
        if not isinstance(announcement_content, str):
            return {"success": False, "message": "Invalid announcement content."}
        self.announcements.append(announcement_content)
        return {"success": True, "message": "Announcement published."}

    def get_power_usage_data(self):
        return {
            "success": True,
            "data": {"power_usage_data": self.power_usage_data}
        }

    def reallocate_sector_power(self, *, sector, power_units):
        if not isinstance(sector, str):
            return {"success": False, "message": "Invalid sector."}
        try:
            power_units = float(power_units)
        except Exception:
            return {"success": False, "message": "Invalid power_units value."}
        self.sector_power[sector] = power_units
        return {"success": True, "message": f"Power for sector {sector} set to {power_units} units."}

    def monitor_energy_usage(self):
        near_limit_sections = []
        for section, info in self.sections.items():
            usage = info.get("usage", 0)
            limit = info.get("limit", 100)
            if usage >= 0.9 * limit:
                near_limit_sections.append(section)
        return {
            "success": True,
            "data": {
                "sections": self.sections,
                "near_limit_sections": near_limit_sections
            }
        }

    def re_allocate_energy_supply(self, *, section, adjustment_percentage):
        if not isinstance(section, str) or not isinstance(adjustment_percentage, str):
            return {"success": False, "message": "Invalid input types."}
        if section not in self.sections:
            self.sections[section] = {"usage": 0, "limit": 100}
        self.sections[section]["adjustment"] = adjustment_percentage
        return {"success": True, "message": f"Energy supply for section {section} adjusted by {adjustment_percentage}."}

    def list_buildings(self):
        return {
            "success": True,
            "data": {"buildings": self.buildings}
        }

    def transmit_power(self, *, from_building_id, to_building_id, amount):
        if not isinstance(from_building_id, str) or not isinstance(to_building_id, str):
            return {"success": False, "message": "Invalid building IDs."}
        try:
            amount = int(amount)
        except Exception:
            return {"success": False, "message": "Amount must be integer."}
        from_building = None
        to_building = None
        for b in self.buildings:
            if b.get("id") == from_building_id:
                from_building = b
            if b.get("id") == to_building_id:
                to_building = b
        if from_building is None or to_building is None:
            return {"success": False, "message": "Building not found."}
        from_building["power"] = from_building.get("power", 0) - amount
        to_building["power"] = to_building.get("power", 0) + amount
        return {"success": True, "message": f"Transferred {amount} kWh from {from_building_id} to {to_building_id}."}

    def list_grids_status(self):
        return {
            "success": True,
            "data": {"grid_status": self.grid_status}
        }

    def reallocate_power(self, *, from_grid_id, to_grid_id, amount):
        if not isinstance(from_grid_id, str) or not isinstance(to_grid_id, str):
            return {"success": False, "message": "Invalid grid IDs."}
        try:
            amount = float(amount)
        except Exception:
            return {"success": False, "message": "Amount must be a number."}
        from_grid = None
        to_grid = None
        for g in self.grids:
            if g.get("id") == from_grid_id:
                from_grid = g
            if g.get("id") == to_grid_id:
                to_grid = g
        if from_grid is None or to_grid is None:
            return {"success": False, "message": "Grid not found."}
        from_grid["power"] = from_grid.get("power", 0) - amount
        to_grid["power"] = to_grid.get("power", 0) + amount
        return {"success": True, "message": f"Reallocated {amount} units from grid {from_grid_id} to {to_grid_id}."}