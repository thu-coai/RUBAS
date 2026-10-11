from BaseEnv import BaseEnv

class SmartWasteManagement(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.waste_data = self.parameters.get("waste_data", [])
        self.reports = self.parameters.get("reports", [])
        self.collection_schedules = self.parameters.get("collection_schedules", {})
        self.waste_sites = self.parameters.get("waste_sites", [])
        self.population_density = self.parameters.get("population_density", {})
        self.next_report_id = 1

    def waste_data_analysis(self, *, category):
        filtered = [d for d in self.waste_data if d.get("category") == category]
        analysis = {
            "category": category,
            "count": len(filtered),
            "trend": "stable" if len(filtered) < 5 else "increasing",
            "projection": len(filtered) + 2
        }
        return {"success": True, "data": analysis}

    def report_generator(self, *, title, content):
        report = {
            "id": str(self.next_report_id),
            "title": title,
            "content": content
        }
        self.reports.append(report)
        self.next_report_id += 1
        return {"success": True, "data": {"report_id": report["id"]}}

    def retrieve_data(self, *, month):
        data = [d for d in self.waste_data if d.get("month") == month]
        return {"success": True, "data": {"waste_data": data}}

    def generate_report(self, *, month):
        data = [d for d in self.waste_data if d.get("month") == month]
        report = {
            "id": str(self.next_report_id),
            "title": f"Waste Report for {month}",
            "content": f"Data count: {len(data)}"
        }
        self.reports.append(report)
        self.next_report_id += 1
        return {"success": True, "data": {"report_id": report["id"], "summary": report["content"]}}

    def remove_report(self, *, report_id):
        before = len(self.reports)
        self.reports = [r for r in self.reports if r.get("id") != report_id]
        after = len(self.reports)
        if before == after:
            return {"success": False, "message": "Report not found."}
        return {"success": True, "message": "Report removed."}

    def review_waste_data(self):
        needs = "No scheduling changes needed." if len(self.waste_data) < 10 else "Consider increasing pickups."
        return {"success": True, "data": {"scheduling_needs": needs}}

    def adjust_pickup_schedule(self, *, location, new_frequency):
        self.collection_schedules[location] = new_frequency
        return {"success": True, "message": f"Pickup schedule for {location} set to {new_frequency}."}

    def review_population_density(self):
        return {"success": True, "data": {"population_density": self.population_density}}

    def skip_collection(self, *, areas_to_skip):
        for area in areas_to_skip:
            self.collection_schedules[area] = "skipped"
        return {"success": True, "message": f"Collection skipped for: {', '.join(areas_to_skip)}"}

    def adjust_collection_schedule(self, *, zone_id, new_schedule):
        self.collection_schedules[zone_id] = new_schedule
        return {"success": True, "message": f"Collection schedule for zone {zone_id} updated."}

    def list_waste_data(self):
        return {"success": True, "data": {"waste_data": self.waste_data}}

    def get_collection_schedule(self):
        return {"success": True, "data": {"collection_schedules": self.collection_schedules}}

    def update_collection_schedule(self, *, location, worker, new_days, new_time):
        self.collection_schedules[location] = {
            "worker": worker,
            "days": new_days,
            "time": new_time
        }
        return {"success": True, "message": f"Schedule updated for {location}."}

    def list_waste_sites(self):
        return {"success": True, "data": {"waste_sites": self.waste_sites}}

    def update_waste_inventory(self, *, site_name, new_level):
        found = False
        for site in self.waste_sites:
            if site.get("name") == site_name:
                site["level"] = new_level
                found = True
                break
        if not found:
            self.waste_sites.append({"name": site_name, "level": new_level})
        return {"success": True, "message": f"Waste inventory for {site_name} updated."}