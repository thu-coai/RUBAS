from BaseEnv import BaseEnv

class AdaptiveAccessControl(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.user_groups = self.parameters.get("user_groups", {
            "admins": {"resources": {"server": ["read", "write", "execute"], "database": ["read", "write"]}},
            "employees": {"resources": {"server": ["read"], "database": ["read"]}}
        })
        self.users = self.parameters.get("users", [
            {"username": "alice", "group": "admins", "access": ["server", "database"]},
            {"username": "bob", "group": "employees", "access": ["server"]}
        ])
        self.files = self.parameters.get("files", [
            {"id": "file1", "name": "report.pdf", "permissions": {"alice": "read", "bob": "read"}},
            {"id": "file2", "name": "data.csv", "permissions": {"alice": "write"}}
        ])

    def modify_access_levels(self, *, user_group, resources):
        if user_group not in self.user_groups:
            return {"success": False, "message": f"User group '{user_group}' not found."}
        for resource, levels in resources.items():
            if not isinstance(levels, list) or not all(l in ["read", "write", "execute"] for l in levels):
                return {"success": False, "message": f"Invalid access levels for resource '{resource}'."}
            self.user_groups[user_group]["resources"][resource] = levels
        return {"success": True, "message": f"Access levels for group '{user_group}' updated."}

    def list_users_access(self):
        data = []
        for user in self.users:
            data.append({
                "username": user["username"],
                "group": user.get("group", ""),
                "access": user.get("access", [])
            })
        return {"success": True, "data": {"users": data}}

    def modify_user_access(self, *, username, access_changes):
        user = next((u for u in self.users if u["username"] == username), None)
        if not user:
            return {"success": False, "message": f"User '{username}' not found."}
        grant = access_changes.get("grant", [])
        revoke = access_changes.get("revoke", [])
        if not isinstance(grant, list) or not isinstance(revoke, list):
            return {"success": False, "message": "Invalid access_changes format."}
        for resource in grant:
            if resource not in user["access"]:
                user["access"].append(resource)
        for resource in revoke:
            if resource in user["access"]:
                user["access"].remove(resource)
        return {"success": True, "message": f"Access for user '{username}' updated."}

    def list_files(self):
        return {"success": True, "data": {"files": self.files}}

    def cancel_file_permission(self, *, file_id, account_name):
        file = next((f for f in self.files if f["id"] == file_id), None)
        if not file:
            return {"success": False, "message": f"File '{file_id}' not found."}
        if account_name in file.get("permissions", {}):
            del file["permissions"][account_name]
            return {"success": True, "message": f"Permission for '{account_name}' cancelled on file '{file_id}'."}
        else:
            return {"success": False, "message": f"Account '{account_name}' does not have permission on file '{file_id}'."}

    def review_existing_access(self):
        groups = []
        for group_name, group_info in self.user_groups.items():
            groups.append({
                "group": group_name,
                "resources": group_info.get("resources", {})
            })
        return {"success": True, "data": {"user_groups": groups}}