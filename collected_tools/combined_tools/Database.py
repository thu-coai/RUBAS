from BaseEnv import BaseEnv

class Database(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.databases = self.parameters.get("databases", [
            {"name": "main_db", "status": "running"},
            {"name": "analytics_db", "status": "running"}
        ])

    def list_databases(self):
        db_list = [{"name": db["name"], "status": db["status"]} for db in self.databases]
        return {"success": True, "data": {"databases": db_list}}

    def shutdown_database(self, *, database_name):
        for db in self.databases:
            if db["name"] == database_name:
                if db["status"] == "stopped":
                    return {"success": False, "message": f"Database '{database_name}' is already stopped."}
                db["status"] = "stopped"
                return {"success": True, "message": f"Database '{database_name}' has been shut down."}
        return {"success": False, "message": f"Database '{database_name}' not found."}