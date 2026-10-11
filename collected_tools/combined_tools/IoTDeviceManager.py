from BaseEnv import BaseEnv

class IoTDeviceManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.devices = self.parameters.get("devices", [
            {"id": "dev1", "name": "Thermostat", "status": "off", "settings": {}, "temperature": "72°F"},
            {"id": "dev2", "name": "AirConditioner", "status": "off", "mode": "cool"},
            {"id": "dev3", "name": "TV", "status": "off", "volume": "10dB"}
        ])
        self.tasks = self.parameters.get("tasks", [
            {"id": "task1", "device_id": "dev1", "description": "Morning temperature adjustment"},
            {"id": "task2", "device_id": "dev2", "description": "Evening cooling"}
        ])
        self.home_status = self.parameters.get("home_status", {"occupied": True, "alarm": "off"})

    def clear_task_assignments(self, *, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                return {"success": True, "message": f"Task {task_id} cleared."}
        return {"success": False, "message": f"Task {task_id} not found."}

    def list_tasks(self):
        return {"success": True, "data": {"tasks": self.tasks}}

    def configure_device(self, *, device_id, settings):
        for device in self.devices:
            if device["id"] == device_id:
                device["settings"].update(settings)
                return {"success": True, "message": f"Device {device_id} configured.", "data": {"device": device}}
        return {"success": False, "message": f"Device {device_id} not found."}

    def list_devices(self):
        return {"success": True, "data": {"devices": self.devices}}

    def adjust_temperature(self, *, device_id, temperature):
        for device in self.devices:
            if device["id"] == device_id:
                device["temperature"] = temperature
                return {"success": True, "message": f"Temperature set to {temperature} for device {device_id}."}
        return {"success": False, "message": f"Device {device_id} not found."}

    def check_home_status(self):
        return {"success": True, "data": {"home_status": self.home_status}}

    def turn_on_air_conditioner(self, *, mode):
        for device in self.devices:
            if device["name"].lower() == "airconditioner":
                device["status"] = "on"
                device["mode"] = mode
                return {"success": True, "message": f"Air conditioner turned on in {mode} mode."}
        return {"success": False, "message": "Air conditioner not found."}

    def change_TV_volume(self, *, volume):
        for device in self.devices:
            if device["name"].lower() == "tv":
                device["volume"] = volume
                return {"success": True, "message": f"TV volume set to {volume}."}
        return {"success": False, "message": "TV not found."}

    def get_device_status(self):
        status_list = []
        for device in self.devices:
            status_list.append({"id": device["id"], "name": device["name"], "status": device.get("status", "unknown")})
        return {"success": True, "data": {"device_status": status_list}}

    def turn_on_device(self, *, device_name):
        for device in self.devices:
            if device["name"].lower() == device_name.lower():
                device["status"] = "on"
                return {"success": True, "message": f"{device_name} turned on."}
        return {"success": False, "message": f"Device {device_name} not found."}