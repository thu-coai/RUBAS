from BaseEnv import BaseEnv

class Health(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.doctors = self.parameters.get("doctors", [])
        self.patients = self.parameters.get("patients", [])
        self.appointments = self.parameters.get("appointments", [])
        self.health_data = self.parameters.get("health_data", {})
        self.user_health_data = self.parameters.get("user_health_data", {})
        self.health_tips_sent = []

    def search_doctors(self, *, search_text):
        res = []
        for doctor in self.doctors:
            if search_text.lower() in doctor.get("name", "").lower():
                res.append(doctor)
        return {"success": True, "data": {"doctors": res}}

    def search_patients(self, *, search_text, search_id):
        res = []
        for patient in self.patients:
            if (search_text.lower() in patient.get("name", "").lower() or
                search_id == patient.get("id", "")):
                res.append(patient)
        return {"success": True, "data": {"patients": res}}

    def update_patient_medications(self, *, patient_id, medications):
        for patient in self.patients:
            if patient.get("id", "") == patient_id:
                patient["medications"] = medications
                return {"success": True, "message": "Medications updated."}
        return {"success": False, "message": "Patient not found."}

    def make_appointment(self, *, doctor_id, time):
        appointment_id = f"appt_{len(self.appointments)+1}"
        appointment = {
            "id": appointment_id,
            "doctor_id": doctor_id,
            "time": time
        }
        self.appointments.append(appointment)
        return {"success": True, "data": {"appointment_id": appointment_id}}

    def search_appointments(self, *, doctor_id):
        res = []
        for appt in self.appointments:
            if appt.get("doctor_id", "") == doctor_id:
                res.append(appt)
        return {"success": True, "data": {"appointments": res}}

    def cancel_appointment(self, *, appointment_id):
        for appt in self.appointments:
            if appt.get("id", "") == appointment_id:
                self.appointments.remove(appt)
                return {"success": True, "message": "Appointment cancelled."}
        return {"success": False, "message": "Appointment not found."}

    def query_health_data(self, *, patient_id):
        data = self.health_data.get(patient_id, {})
        return {"success": True, "data": {"health_data": data}}

    def record_health_data(self, *, patient_id, blood_pressure, heart_rate):
        self.health_data[patient_id] = {
            "blood_pressure": blood_pressure,
            "heart_rate": heart_rate
        }
        return {"success": True, "message": "Health data recorded."}

    def search_symptoms(self, *, symptom_text):
        # Simulate: just echo the symptom
        return {"success": True, "data": {"symptom": symptom_text, "info": "Symptom information not available in simulation."}}

    def search_guidelines(self, *, search_item):
        # Simulate: return a mock guideline
        return {"success": True, "data": {"guidelines": f"General care guidelines for {search_item} (not verified)."}}

    def get_user_health_data(self):
        return {"success": True, "data": {"user_health_data": self.user_health_data}}

    def search_health_tips(self, *, health_situation):
        # Simulate: return a mock tip
        return {"success": True, "data": {"tips": [f"Tip for {health_situation}: Stay hydrated and rest."]}}

    def send_health_tips(self, *, content):
        self.health_tips_sent.append(content)
        return {"success": True, "message": "Health tip sent."}

    def provide_health_suggestions(self):
        # Simulate: return a mock suggestion
        return {"success": True, "data": {"suggestions": ["Exercise regularly.", "Eat balanced meals.", "Get enough sleep."]}}