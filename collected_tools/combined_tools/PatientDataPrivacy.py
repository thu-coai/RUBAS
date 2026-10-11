from BaseEnv import BaseEnv

class PatientDataPrivacy(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.patient_records = self.parameters.get("patient_records", [])
        self.insurance_providers = self.parameters.get("insurance_providers", [])
        self.default_insurance_provider_id = self.parameters.get("default_insurance_provider_id", None)
        self.user_access_rights = self.parameters.get("user_access_rights", {})
        self.medicine_recommendations = self.parameters.get("medicine_recommendations", {})

    def list_patient_records(self):
        return {"success": True, "data": {"patient_records": self.patient_records}}

    def merge_duplicate_records(self, *, primary_record_id, duplicate_record_id):
        primary = None
        duplicate = None
        for record in self.patient_records:
            if record.get("id") == primary_record_id:
                primary = record
            if record.get("id") == duplicate_record_id:
                duplicate = record
        if not primary or not duplicate:
            return {"success": False, "message": "One or both records not found."}
        for key, value in duplicate.items():
            if key not in primary or not primary[key]:
                primary[key] = value
        self.patient_records = [r for r in self.patient_records if r.get("id") != duplicate_record_id]
        return {"success": True, "message": "Records merged."}

    def delete_patient_record(self, *, record_id):
        before = len(self.patient_records)
        self.patient_records = [r for r in self.patient_records if r.get("id") != record_id]
        after = len(self.patient_records)
        if before == after:
            return {"success": False, "message": "Record not found."}
        return {"success": True, "message": "Record deleted."}

    def list_insurance_providers(self):
        return {"success": True, "data": {"insurance_providers": self.insurance_providers}}

    def update_insurance_provider(self, *, new_provider_id):
        found = False
        for provider in self.insurance_providers:
            if provider.get("id") == new_provider_id:
                found = True
                break
        if not found:
            return {"success": False, "message": "Provider not found."}
        self.default_insurance_provider_id = new_provider_id
        return {"success": True, "message": "Default insurance provider updated."}

    def modify_access_rights(self, *, user_group, access_rights):
        if not isinstance(access_rights, list):
            return {"success": False, "message": "access_rights must be a list."}
        self.user_access_rights[user_group] = access_rights
        return {"success": True, "message": f"Access rights updated for {user_group}."}

    def get_current_user_access_levels(self):
        return {"success": True, "data": {"user_access_rights": self.user_access_rights}}

    def get_patient_info(self, *, patient_id):
        for record in self.patient_records:
            if record.get("id") == patient_id:
                return {"success": True, "data": {"patient_info": record}}
        return {"success": False, "message": "Patient not found."}

    def recommend_medicine(self, *, medicine_name):
        # Just simulate a recommendation
        return {"success": True, "message": f"Medicine '{medicine_name}' is recommended."}

    def update_medication(self, *, patient_id, new_medications):
        if not isinstance(new_medications, list):
            return {"success": False, "message": "new_medications must be a list."}
        for record in self.patient_records:
            if record.get("id") == patient_id:
                meds = record.get("medications", [])
                meds.extend(new_medications)
                record["medications"] = list(set(meds))
                return {"success": True, "message": "Medications updated."}
        return {"success": False, "message": "Patient not found."}