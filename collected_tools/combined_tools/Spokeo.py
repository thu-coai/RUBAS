from BaseEnv import BaseEnv

class Spokeo(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.people = self.parameters.get("people", [])
        self.public_records = self.parameters.get("public_records", {})
        self.data_changes = {}
        self.court_records = self.parameters.get("court_records", {})
        self.criminal_histories = self.parameters.get("criminal_histories", {})
        self.phone_index = {}
        for person in self.people:
            phone = person.get("phone")
            if phone:
                self.phone_index[phone] = person

    def search_people(self, *, search_term, search_type, max_results=10):
        if search_type not in ["name", "email", "phone", "address"]:
            return {"success": False, "message": "Invalid search_type."}
        results = []
        for person in self.people:
            value = person.get(search_type)
            if value and search_term.lower() in str(value).lower():
                results.append(person)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"results": results}}

    def get_person_details(self, *, unique_id):
        for person in self.people:
            if person.get("id") == unique_id:
                return {"success": True, "data": {"person": person}}
        return {"success": False, "message": "Person not found."}

    def background_check(self, *, unique_id):
        for person in self.people:
            if person.get("id") == unique_id:
                return {"success": True, "data": {"background_check": {"status": "clear"}}}
        return {"success": False, "message": "Person not found."}

    def verify_identity(self, *, unique_id, provided_data):
        for person in self.people:
            if person.get("id") == unique_id:
                match = all(person.get(k) == v for k, v in provided_data.items())
                return {"success": True, "data": {"verified": match}}
        return {"success": False, "message": "Person not found."}

    def monitor_data_changes(self, *, unique_id):
        changes = self.data_changes.get(unique_id, [])
        return {"success": True, "data": {"changes": changes}}

    def get_historical_data(self, *, unique_id):
        for person in self.people:
            if person.get("id") == unique_id:
                history = person.get("history", [])
                return {"success": True, "data": {"historical_data": history}}
        return {"success": False, "message": "Person not found."}

    def access_court_records(self, *, unique_id):
        records = self.court_records.get(unique_id, [])
        return {"success": True, "data": {"court_records": records}}

    def get_criminal_history(self, *, unique_id):
        history = self.criminal_histories.get(unique_id, [])
        return {"success": True, "data": {"criminal_history": history}}

    def reverse_phone_lookup(self, *, phone_number):
        person = self.phone_index.get(phone_number)
        if person:
            return {"success": True, "data": {"person": person}}
        return {"success": False, "message": "No match found for phone number."}

    def download_public_record(self, *, unique_id, record_id, local_file_path):
        records = self.public_records.get(unique_id, {})
        record = records.get(record_id)
        if record:
            # Simulate saving the record
            return {"success": True, "message": f"Record saved to {local_file_path}."}
        return {"success": False, "message": "Record not found."}