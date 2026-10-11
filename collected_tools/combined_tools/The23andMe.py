from BaseEnv import BaseEnv

class The23andMe(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.genetic_data = self.parameters.get("genetic_data", {
            "ancestry": "Unknown",
            "traits": "Unknown",
            "health_predispositions": "Unknown",
            "carrier_status": "Unknown"
        })
        self.privacy_settings = self.parameters.get("privacy_settings", {
            "share_with_third_parties": False,
            "allow_download": False
        })
        self.third_party_apps = self.parameters.get("third_party_apps", ["app_1", "app_2"])
        self.shared_with = set()

    def get_genetic_data(self):
        if self.genetic_data is None:
            return {"success": False, "message": "No genetic data available."}
        return {"success": True, "data": self.genetic_data}

    def get_health_recommendations(self):
        if self.genetic_data is None:
            return {"success": False, "message": "No genetic data available."}
        recommendations = f"Based on your health predispositions: {self.genetic_data.get('health_predispositions', 'Unknown')}, maintain a healthy lifestyle."
        return {"success": True, "data": {"recommendations": recommendations}}

    def get_genetic_insights(self):
        if self.genetic_data is None:
            return {"success": False, "message": "No genetic data available."}
        insights = {
            "ancestry": f"Your ancestry is {self.genetic_data.get('ancestry', 'Unknown')}.",
            "traits": f"Traits: {self.genetic_data.get('traits', 'Unknown')}.",
            "carrier_status": f"Carrier status: {self.genetic_data.get('carrier_status', 'Unknown')}."
        }
        return {"success": True, "data": {"insights": insights}}

    def set_data_privacy(self, *, privacy_settings):
        if not isinstance(privacy_settings, dict):
            return {"success": False, "message": "privacy_settings must be an object."}
        required = ["share_with_third_parties", "allow_download"]
        for key in required:
            if key not in privacy_settings:
                return {"success": False, "message": f"Missing required privacy setting: {key}."}
            if not isinstance(privacy_settings[key], bool):
                return {"success": False, "message": f"{key} must be a boolean."}
        self.privacy_settings = privacy_settings
        return {"success": True, "message": "Privacy settings updated."}

    def list_third_party_apps(self):
        return {"success": True, "data": {"third_party_apps": self.third_party_apps}}

    def ShareData(self, *, app_id):
        if app_id not in self.third_party_apps:
            return {"success": False, "message": "Invalid app_id."}
        if not self.privacy_settings.get("share_with_third_parties", False):
            return {"success": False, "message": "Sharing with third parties is disabled in privacy settings."}
        self.shared_with.add(app_id)
        return {"success": True, "message": f"Genetic data shared with {app_id}."}

    def download_data(self):
        if not self.privacy_settings.get("allow_download", False):
            return {"success": False, "message": "Download not allowed by privacy settings."}
        if self.genetic_data is None:
            return {"success": False, "message": "No genetic data available."}
        return {"success": True, "data": self.genetic_data}

    def update_data(self, *, new_data):
        required = ["ancestry", "traits", "health_predispositions", "carrier_status"]
        if not isinstance(new_data, dict):
            return {"success": False, "message": "new_data must be an object."}
        for key in required:
            if key not in new_data:
                return {"success": False, "message": f"Missing required field in new_data: {key}."}
        self.genetic_data = new_data
        return {"success": True, "message": "Genetic data updated."}

    def delete_data(self):
        self.genetic_data = None
        return {"success": True, "message": "Genetic data deleted."}