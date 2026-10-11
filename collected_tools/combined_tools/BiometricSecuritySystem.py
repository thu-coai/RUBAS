from BaseEnv import BaseEnv

class BiometricSecuritySystem(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.security_logs = self.parameters.get("security_logs", [])
        self.biometric_data = self.parameters.get("biometric_data", {})
        self.access_list = self.parameters.get("access_list", [])
        self.vaults = self.parameters.get("vaults", {})
        self.employees = self.parameters.get("employees", [])
        self.users = self.parameters.get("users", [])
        self.authorized_personnel = self.parameters.get("authorized_personnel", [])
        self.access_requests = self.parameters.get("access_requests", [])
        self.user_biometric_data = self.parameters.get("user_biometric_data", {})

    def get_security_logs(self):
        return {"success": True, "data": {"logs": self.security_logs}}

    def update_access_granted(self, *, access_id, access_granted):
        found = False
        for log in self.security_logs:
            if log.get("id") == access_id:
                log["access_granted"] = access_granted
                found = True
                break
        if found:
            return {"success": True, "message": "Access granted status updated."}
        else:
            return {"success": False, "message": "Access log entry not found."}

    def get_biometric_data(self):
        return {"success": True, "data": {"biometric_data": self.biometric_data, "logs": self.security_logs}}

    def control_security_system(self, *, location, target_status):
        if "gates" not in self.biometric_data:
            self.biometric_data["gates"] = {}
        self.biometric_data["gates"][location] = target_status
        return {"success": True, "message": f"Security system at {location} set to {target_status}."}

    def add_into_access_list(self, *, name):
        if name not in self.access_list:
            self.access_list.append(name)
            return {"success": True, "message": f"{name} added to access list."}
        else:
            return {"success": False, "message": f"{name} is already in the access list."}

    def get_vault_status(self):
        return {"success": True, "data": {"vaults": self.vaults}}

    def get_employee_list(self):
        return {"success": True, "data": {"employees": self.employees}}

    def update_vault_security_settings(self, *, vault_name, biometric_threshold):
        if vault_name not in self.vaults:
            self.vaults[vault_name] = {}
        self.vaults[vault_name]["biometric_threshold"] = biometric_threshold
        return {"success": True, "message": f"Vault {vault_name} biometric threshold updated."}

    def list_users(self):
        return {"success": True, "data": {"users": self.users}}

    def reset_biometric_data(self, *, user_id):
        self.user_biometric_data[user_id] = "default"
        return {"success": True, "message": f"Biometric data for user {user_id} reset to default."}

    def list_authorized_personnel(self):
        return {"success": True, "data": {"authorized_personnel": self.authorized_personnel}}

    def list_access_requests(self):
        return {"success": True, "data": {"access_requests": self.access_requests}}

    def grant_access(self, *, name):
        self.access_requests.append({"name": name, "status": "granted"})
        return {"success": True, "message": f"Access granted to {name}."}