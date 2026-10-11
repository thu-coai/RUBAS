from BaseEnv import BaseEnv

class ResourceOptimization(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.systems = self.parameters.get("systems", [
            {"system_id": "sys1", "power_output": "100"},
            {"system_id": "sys2", "power_output": "150"}
        ])
        self.rooms = self.parameters.get("rooms", [
            {"room_id": "room1", "patient_name": None},
            {"room_id": "room2", "patient_name": None}
        ])
        self.logs = self.parameters.get("logs", ["log1", "log2"])
        self.grids = self.parameters.get("grids", [
            {"grid_id": "grid1", "load_mw": 50, "active": True},
            {"grid_id": "grid2", "load_mw": 70, "active": True}
        ])
        self.services = self.parameters.get("services", [
            {"service_id": "svc1", "active": True},
            {"service_id": "svc2", "active": True}
        ])
        self.resources = self.parameters.get("resources", [
            {"resource_id": "res1", "location": "loc1", "quantity": 10},
            {"resource_id": "res2", "location": "loc2", "quantity": 5}
        ])
        self.project_files = self.parameters.get("project_files", ["file1.txt", "file2.txt"])
        self.files = self.parameters.get("files", ["file1.txt", "file2.txt"])
        self.projects = self.parameters.get("projects", [
            {"project_id": "proj1", "name": "Project 1"},
            {"project_id": "proj2", "name": "Project 2"}
        ])
        self.legal_demands = self.parameters.get("legal_demands", ["demand1", "demand2"])
        self.operational_hours = self.parameters.get("operational_hours", "08:00-18:00")

    def monitor_power_levels(self):
        data = [{"system_id": s["system_id"], "power_output": s["power_output"]} for s in self.systems]
        return {"success": True, "data": {"power_levels": data}}

    def adjust_power_output(self, *, system_id, new_power_output):
        found = False
        for s in self.systems:
            if s["system_id"] == system_id:
                s["power_output"] = new_power_output
                found = True
                break
        if not found:
            return {"success": False, "message": f"System {system_id} not found."}
        return {"success": True, "message": f"Power output for {system_id} set to {new_power_output}."}

    def check_room_schedules(self):
        data = [{"room_id": r["room_id"], "patient_name": r["patient_name"]} for r in self.rooms]
        return {"success": True, "data": {"rooms": data}}

    def allocate_room(self, *, patient_name, room_id):
        for r in self.rooms:
            if r["room_id"] == room_id:
                if r["patient_name"] is None:
                    r["patient_name"] = patient_name
                    return {"success": True, "message": f"Patient {patient_name} allocated to room {room_id}."}
                else:
                    return {"success": False, "message": f"Room {room_id} is already occupied."}
        return {"success": False, "message": f"Room {room_id} not found."}

    def share_log_data(self):
        return {"success": True, "data": {"logs": self.logs}}

    def list_grids(self):
        data = [{"grid_id": g["grid_id"], "load_mw": g["load_mw"], "active": g["active"]} for g in self.grids]
        return {"success": True, "data": {"grids": data}}

    def adjust_power_distribution(self, *, source_grid_id, target_grid_id, transfer_mw):
        source = None
        target = None
        for g in self.grids:
            if g["grid_id"] == source_grid_id:
                source = g
            if g["grid_id"] == target_grid_id:
                target = g
        if source is None or target is None:
            return {"success": False, "message": "Source or target grid not found."}
        if not source["active"] or not target["active"]:
            return {"success": False, "message": "One of the grids is not active."}
        if source["load_mw"] < transfer_mw:
            return {"success": False, "message": "Not enough load to transfer from source grid."}
        source["load_mw"] -= transfer_mw
        target["load_mw"] += transfer_mw
        return {"success": True, "message": f"Transferred {transfer_mw} MW from {source_grid_id} to {target_grid_id}."}

    def shutdown_grid(self, *, grid_id):
        for g in self.grids:
            if g["grid_id"] == grid_id:
                g["active"] = False
                return {"success": True, "message": f"Grid {grid_id} shut down."}
        return {"success": False, "message": f"Grid {grid_id} not found."}

    def list_services(self):
        data = [{"service_id": s["service_id"], "active": s["active"]} for s in self.services]
        return {"success": True, "data": {"services": data}}

    def shutdown_services(self, *, service_ids):
        not_found = []
        for sid in service_ids:
            found = False
            for s in self.services:
                if s["service_id"] == sid:
                    s["active"] = False
                    found = True
                    break
            if not found:
                not_found.append(sid)
        if not_found:
            return {"success": False, "message": f"Services not found: {', '.join(not_found)}"}
        return {"success": True, "message": "Services shut down."}

    def list_resources(self):
        data = [{"resource_id": r["resource_id"], "location": r["location"], "quantity": r["quantity"]} for r in self.resources]
        return {"success": True, "data": {"resources": data}}

    def allocate_resource(self, *, resource_id, location, quantity):
        for r in self.resources:
            if r["resource_id"] == resource_id:
                if r["quantity"] < quantity:
                    return {"success": False, "message": "Not enough resource quantity available."}
                r["quantity"] -= quantity
                # Simulate allocation by adding to location (not tracked in detail)
                return {"success": True, "message": f"Allocated {quantity} units of {resource_id} to {location}."}
        return {"success": False, "message": f"Resource {resource_id} not found."}

    def list_project_files(self):
        return {"success": True, "data": {"project_files": self.project_files}}

    def delete_file(self, *, file_name):
        if file_name in self.files:
            self.files.remove(file_name)
            return {"success": True, "message": f"File {file_name} deleted."}
        return {"success": False, "message": f"File {file_name} not found."}

    def list_files(self):
        return {"success": True, "data": {"files": self.files}}

    def list_projects(self):
        return {"success": True, "data": {"projects": self.projects}}

    def data_analysis(self, *, file_name):
        if file_name not in self.files:
            return {"success": False, "message": f"File {file_name} not found."}
        # Simulate analysis
        return {"success": True, "message": f"Data in {file_name} analyzed."}

    def delete_project(self, *, project_id):
        for p in self.projects:
            if p["project_id"] == project_id:
                self.projects.remove(p)
                return {"success": True, "message": f"Project {project_id} deleted."}
        return {"success": False, "message": f"Project {project_id} not found."}

    def optimize_operational_hours(self, *, duration):
        self.operational_hours = duration
        return {"success": True, "message": f"Operational hours set to {duration}."}

    def check_legal_demands(self):
        return {"success": True, "data": {"legal_demands": self.legal_demands}}