from BaseEnv import BaseEnv

class RealEstateAssistant(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.properties = self.parameters.get("properties", [
            {"id": "p1", "address": "123 Main St", "price": 500000, "status": "available"},
            {"id": "p2", "address": "456 Oak Ave", "price": 350000, "status": "available"},
            {"id": "p3", "address": "789 Pine Rd", "price": 420000, "status": "available"}
        ])
        self.shortlist = []

    def gen_script(self, *, requirements):
        script = f"# Script generated for requirements: {requirements}\nprint('This is a mock script for: {requirements}')"
        return {"success": True, "data": {"script": script}}

    def list_properties(self):
        return {"success": True, "data": {"properties": self.properties}}

    def shortlist_property(self, *, property_id):
        for prop in self.properties:
            if prop.get("id") == property_id:
                if property_id not in self.shortlist:
                    self.shortlist.append(property_id)
                return {"success": True, "message": f"Property {property_id} added to shortlist."}
        return {"success": False, "message": f"Property {property_id} not found."}