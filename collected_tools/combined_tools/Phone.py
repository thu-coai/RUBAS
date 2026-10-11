from BaseEnv import BaseEnv

class Phone(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.imei_code = self.parameters.get("imei_code", "000000000000000")
        self.apps = self.parameters.get("apps", [
            {"name": "Calculator", "download_link": "http://appstore/calculator"},
            {"name": "Notes", "download_link": "http://appstore/notes"},
            {"name": "Browser", "download_link": "http://appstore/browser"}
        ])
        self.installed_apps = [app["name"] for app in self.apps]
        self.volume = self.parameters.get("volume", 5)

    def get_IMEI_code(self):
        return {"success": True, "data": {"imei_code": self.imei_code}}

    def search_apps(self, *, search_text):
        if not isinstance(search_text, str):
            return {"success": False, "message": "search_text must be a string."}
        found = [app for app in self.apps if search_text.lower() in app["name"].lower()]
        return {"success": True, "data": {"apps": found}}

    def download_app(self, *, download_link):
        if not isinstance(download_link, str):
            return {"success": False, "message": "download_link must be a string."}
        for app in self.apps:
            if app["download_link"] == download_link:
                if app["name"] not in self.installed_apps:
                    self.installed_apps.append(app["name"])
                return {"success": True, "message": f"App '{app['name']}' downloaded."}
        # Simulate adding a new app if not found
        new_app_name = f"App_{len(self.apps)+1}"
        self.apps.append({"name": new_app_name, "download_link": download_link})
        self.installed_apps.append(new_app_name)
        return {"success": True, "message": f"App '{new_app_name}' downloaded."}

    def delete_apps(self, *, names):
        if not isinstance(names, list):
            return {"success": False, "message": "names must be a list of strings."}
        deleted = []
        for name in names:
            if name in self.installed_apps:
                self.installed_apps.remove(name)
                deleted.append(name)
        return {"success": True, "data": {"deleted": deleted}}

    def open_app(self, *, name):
        if not isinstance(name, str):
            return {"success": False, "message": "name must be a string."}
        if name in self.installed_apps:
            return {"success": True, "message": f"App '{name}' opened."}
        else:
            return {"success": False, "message": f"App '{name}' is not installed."}

    def click_link(self, *, link):
        if not isinstance(link, str):
            return {"success": False, "message": "link must be a string."}
        return {"success": True, "message": f"Link '{link}' clicked."}

    def get_volume(self):
        return {"success": True, "data": {"volume": self.volume}}

    def set_volume(self, *, volume):
        try:
            vol = float(volume)
        except (TypeError, ValueError):
            return {"success": False, "message": "volume must be a number between 0 and 10."}
        if vol < 0 or vol > 10:
            return {"success": False, "message": "volume must be between 0 and 10."}
        self.volume = int(vol) if vol.is_integer() else vol
        return {"success": True, "data": {"volume": self.volume}}