from BaseEnv import BaseEnv

class MedicalDiagnosis(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.patient_info = self.parameters.get("patient_info", {"id": "P001", "name": "John Doe", "age": 40})
        self.test_results = self.parameters.get("test_results", {
            "cholesterol": "200",
            "blood_sugar": "110",
            "thyroid_level": "3.0"
        })
        self.medications = self.parameters.get("medications", [])
        self.appointments = self.parameters.get("appointments", [
            {"patient_id": "P001", "day": "Monday", "time": "10:00 AM"}
        ])
        self.treatments = self.parameters.get("treatments", [])

    def adjust_medication(self, *, medication_adjustments):
        self.medications.append({"adjustment": medication_adjustments})
        return {"success": True, "message": "Medication adjusted.", "data": {"medications": self.medications}}

    def analyze_test_results(self, *, cholesterol, blood_sugar, thyroid_level):
        self.test_results = {
            "cholesterol": cholesterol,
            "blood_sugar": blood_sugar,
            "thyroid_level": thyroid_level
        }
        analysis = "Analysis complete. Possible issues identified."
        return {"success": True, "message": analysis, "data": {"test_results": self.test_results}}

    def get_test_results(self):
        return {"success": True, "data": {"test_results": self.test_results}}

    def get_patient_info(self):
        return {"success": True, "data": {"patient_info": self.patient_info}}

    def suggest_medication(self, *, medication_name, dosage):
        suggestion = {"medication_name": medication_name, "dosage": dosage}
        self.medications.append(suggestion)
        return {"success": True, "message": "Medication suggested.", "data": {"medications": self.medications}}

    def get_appointment_schedule(self):
        return {"success": True, "data": {"appointments": self.appointments}}

    def reschedule_appointment(self, *, patient_id, new_time, new_day):
        found = False
        for appt in self.appointments:
            if appt.get("patient_id") == patient_id:
                appt["time"] = new_time
                appt["day"] = new_day
                found = True
                break
        if not found:
            self.appointments.append({"patient_id": patient_id, "day": new_day, "time": new_time})
        return {"success": True, "message": "Appointment rescheduled.", "data": {"appointments": self.appointments}}

    def recommend_treatment(self, *, symptom):
        treatment = f"Recommended treatment for {symptom}."
        self.treatments.append({"symptom": symptom, "recommendation": treatment})
        return {"success": True, "message": treatment, "data": {"treatments": self.treatments}}