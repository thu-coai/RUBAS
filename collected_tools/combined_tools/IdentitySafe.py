from BaseEnv import BaseEnv

class IdentitySafe(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.passwords = self.parameters.get("passwords", [])
        self.personal_info = self.parameters.get("personal_info", {"address": [], "payment": []})
        self.two_factor_enabled = False
        self.two_factor_phone = None

    def store_password(self, *, password, website, username):
        entry = {
            "password": password,
            "website": website,
            "username": username
        }
        self.passwords.append(entry)
        return {"success": True, "message": "Password stored successfully."}

    def check_password_strength(self, *, password):
        if not isinstance(password, str):
            return {"success": False, "message": "Password must be a string."}
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        score = sum([has_upper, has_lower, has_digit, has_symbol])
        if length >= 12 and score == 4:
            strength = "strong"
        elif length >= 8 and score >= 3:
            strength = "medium"
        else:
            strength = "weak"
        return {"success": True, "data": {"strength": strength}}

    def generate_password(
        self,
        *,
        strength,
        length=12,
        include_symbols=True,
        include_numbers=True,
        include_uppercase=True,
        include_lowercase=True
    ):
        if strength not in ["weak", "medium", "strong"]:
            return {"success": False, "message": "Invalid strength value."}
        # Simulate password generation
        base = ""
        if include_lowercase:
            base += "abcdefghijklmnopqrstuvwxyz"
        if include_uppercase:
            base += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if include_numbers:
            base += "0123456789"
        if include_symbols:
            base += "!@#$%^&*()-_=+[]{}|;:,.<>/?"
        if not base:
            base = "password"
        # Just mock a password string
        password = (base[:length] * ((length // len(base)) + 1))[:length]
        return {"success": True, "data": {"password": password, "strength": strength}}

    def auto_fill_password(self, *, website):
        matches = [p for p in self.passwords if p["website"] == website]
        if matches:
            return {"success": True, "data": {"website": website, "username": matches[0]["username"], "password": matches[0]["password"]}}
        else:
            return {"success": False, "message": "No password found for the specified website."}

    def search_passwords(self, *, query, max_results=10):
        results = []
        for entry in self.passwords:
            if query in entry.get("website", "") or query in entry.get("username", ""):
                results.append(entry)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"passwords": results}}

    def store_personal_info(self, *, info_type, info_data):
        if info_type not in ["address", "payment"]:
            return {"success": False, "message": "Invalid info_type."}
        if not isinstance(info_data, dict):
            return {"success": False, "message": "info_data must be an object."}
        self.personal_info.setdefault(info_type, []).append(info_data)
        return {"success": True, "message": f"{info_type.capitalize()} information stored successfully."}

    def auto_fill_personal_info(self, *, website, info_type):
        if info_type not in ["address", "payment"]:
            return {"success": False, "message": "Invalid info_type."}
        info_list = self.personal_info.get(info_type, [])
        if info_list:
            return {"success": True, "data": {"website": website, "info_type": info_type, "info_data": info_list[0]}}
        else:
            return {"success": False, "message": f"No {info_type} information stored."}

    def retrieve_personal_info(self, *, info_type):
        if info_type not in ["address", "payment"]:
            return {"success": False, "message": "Invalid info_type."}
        info_list = self.personal_info.get(info_type, [])
        return {"success": True, "data": {info_type: info_list}}

    def share_password(self, *, website, username, contact_email):
        matches = [p for p in self.passwords if p["website"] == website and p["username"] == username]
        if matches:
            # Simulate sharing
            return {"success": True, "message": f"Password shared with {contact_email}."}
        else:
            return {"success": False, "message": "No matching password found to share."}

    def import_passwords(self, *, file_path):
        # Simulate import by adding a mock password
        self.passwords.append({"password": "imported_pass", "website": "imported.com", "username": "imported_user"})
        return {"success": True, "message": f"Passwords imported from {file_path}."}

    def export_passwords(self, *, file_path):
        # Simulate export
        return {"success": True, "message": f"Passwords exported to {file_path}."}

    def enable_two_factor_authentication(self, *, phone_number):
        self.two_factor_enabled = True
        self.two_factor_phone = phone_number
        return {"success": True, "message": "Two-factor authentication enabled."}

    def disable_two_factor_authentication(self):
        self.two_factor_enabled = False
        self.two_factor_phone = None
        return {"success": True, "message": "Two-factor authentication disabled."}