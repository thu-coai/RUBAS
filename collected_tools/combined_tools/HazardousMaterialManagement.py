from BaseEnv import BaseEnv

class HazardousMaterialManagement(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.materials = self.parameters.get("materials", [])
        self.facilities = self.parameters.get("facilities", [])
        self.vehicles = self.parameters.get("vehicles", [])
        self.containers = self.parameters.get("containers", [])
        self.routes = self.parameters.get("routes", [])
        self.transport_assignments = []
        self.inventory = {m.get("id", ""): m.get("quantity", 0) for m in self.materials}
        self.material_locations = {m.get("id", ""): m.get("location", "") for m in self.materials}
        self.material_vehicle = {}
        self.container_allocations = []

    def throw_away(self, *, material_name):
        found = False
        for m in self.materials:
            if m.get("name", "") == material_name:
                self.materials.remove(m)
                self.inventory.pop(m.get("id", ""), None)
                self.material_locations.pop(m.get("id", ""), None)
                found = True
                break
        if found:
            return {"success": True, "message": f"Material '{material_name}' disposed."}
        else:
            return {"success": False, "message": f"Material '{material_name}' not found."}

    def list_materials(self):
        return {"success": True, "data": {"materials": self.materials}}

    def relocate_material(self, *, material_id, new_location):
        for m in self.materials:
            if m.get("id", "") == material_id:
                m["location"] = new_location
                self.material_locations[material_id] = new_location
                return {"success": True, "message": f"Material '{material_id}' relocated to '{new_location}'."}
        return {"success": False, "message": f"Material '{material_id}' not found."}

    def list_facilities(self):
        return {"success": True, "data": {"facilities": self.facilities}}

    def list_vehicles(self):
        return {"success": True, "data": {"vehicles": self.vehicles}}

    def assign_transport_vehicle(self, *, vehicle_id, material_id):
        vehicle_exists = any(v.get("id", "") == vehicle_id for v in self.vehicles)
        material_exists = any(m.get("id", "") == material_id for m in self.materials)
        if not vehicle_exists:
            return {"success": False, "message": f"Vehicle '{vehicle_id}' not found."}
        if not material_exists:
            return {"success": False, "message": f"Material '{material_id}' not found."}
        self.material_vehicle[material_id] = vehicle_id
        return {"success": True, "message": f"Vehicle '{vehicle_id}' assigned to material '{material_id}'."}

    def update_inventory(self, *, material_id, quantity):
        if material_id not in self.inventory:
            return {"success": False, "message": f"Material '{material_id}' not found in inventory."}
        self.inventory[material_id] = quantity
        for m in self.materials:
            if m.get("id", "") == material_id:
                m["quantity"] = quantity
        return {"success": True, "message": f"Inventory for material '{material_id}' updated to {quantity}."}

    def refer_guidelines(self, *, material):
        return {"success": True, "data": {"guidelines": f"Mock guidelines for handling '{material}'."}}

    def get_disposal_guidelines(self, *, material):
        return {"success": True, "data": {"guidelines": f"Mock disposal guidelines for '{material}'."}}

    def check_regulations(self, *, route_id):
        route_exists = any(r.get("id", "") == route_id for r in self.routes)
        if not route_exists:
            return {"success": False, "message": f"Route '{route_id}' not found."}
        return {"success": True, "data": {"regulations": f"Mock regulations for route '{route_id}'."}}

    def get_delivery_status(self, *, route_id):
        route_exists = any(r.get("id", "") == route_id for r in self.routes)
        if not route_exists:
            return {"success": False, "message": f"Route '{route_id}' not found."}
        return {"success": True, "data": {"status": f"Mock delivery status for route '{route_id}'."}}

    def list_containers(self):
        return {"success": True, "data": {"containers": self.containers}}

    def allocate_transport_resources(self, *, container_id, route_id):
        container_exists = any(c.get("id", "") == container_id for c in self.containers)
        route_exists = any(r.get("id", "") == route_id for r in self.routes)
        if not container_exists:
            return {"success": False, "message": f"Container '{container_id}' not found."}
        if not route_exists:
            return {"success": False, "message": f"Route '{route_id}' not found."}
        self.container_allocations.append({"container_id": container_id, "route_id": route_id})
        return {"success": True, "message": f"Container '{container_id}' allocated to route '{route_id}'."}