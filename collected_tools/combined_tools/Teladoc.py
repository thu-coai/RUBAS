from BaseEnv import BaseEnv

class Teladoc(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.doctors = self.parameters.get("doctors", [
            {"id": "doc1", "name": "Dr. Smith", "specialty": "Cardiology", "location": "NY", "available_dates": ["2024-06-01", "2024-06-02"]},
            {"id": "doc2", "name": "Dr. Lee", "specialty": "Dermatology", "location": "CA", "available_dates": ["2024-06-01", "2024-06-03"]},
        ])
        self.user_info = self.parameters.get("user_info", {
            "date_of_birth": "1990-01-01",
            "location": "NY",
            "familial_genetic_diseases": ["None"],
            "allergies": ["Peanuts"],
            "medications": ["Aspirin"],
            "immunizations": ["MMR"]
        })
        self.medical_history = self.parameters.get("medical_history", [
            {"date": "2023-01-01", "description": "Annual checkup"},
            {"date": "2023-06-01", "description": "Allergy test"}
        ])
        self.appointments = self.parameters.get("appointments", [])
        self.consultations = self.parameters.get("consultations", [])
        self.prescriptions = self.parameters.get("prescriptions", [])
        self.reviews = self.parameters.get("reviews", [])
        self.next_appointment_id = 1
        self.next_consultation_id = 1

    def search_doctors(self, *, keywords, location, date):
        results = []
        for doctor in self.doctors:
            if (keywords.lower() in doctor.get("name", "").lower() or
                keywords.lower() in doctor.get("specialty", "").lower()) and \
                location.lower() == doctor.get("location", "").lower() and \
                date in doctor.get("available_dates", []):
                results.append(doctor)
        return {"success": True, "data": {"doctors": results}}

    def consult_doctor(self, *, doctor_id, reason):
        doctor = next((d for d in self.doctors if d["id"] == doctor_id), None)
        if not doctor:
            return {"success": False, "message": "Doctor not found."}
        consultation_id = f"consult{self.next_consultation_id}"
        self.next_consultation_id += 1
        consultation = {
            "id": consultation_id,
            "doctor_id": doctor_id,
            "reason": reason,
            "messages": []
        }
        self.consultations.append(consultation)
        return {"success": True, "data": {"consultation_id": consultation_id}}

    def schedule_appointment(self, *, doctor_id, date, time, reason):
        doctor = next((d for d in self.doctors if d["id"] == doctor_id), None)
        if not doctor:
            return {"success": False, "message": "Doctor not found."}
        appointment_id = f"appt{self.next_appointment_id}"
        self.next_appointment_id += 1
        appointment = {
            "id": appointment_id,
            "doctor_id": doctor_id,
            "date": date,
            "time": time,
            "reason": reason,
            "status": "scheduled"
        }
        self.appointments.append(appointment)
        return {"success": True, "data": {"appointment_id": appointment_id}}

    def manage_appointments(self, *, appointment_id, action, date=None, time=None):
        appointment = next((a for a in self.appointments if a["id"] == appointment_id), None)
        if not appointment:
            return {"success": False, "message": "Appointment not found."}
        if action == "view":
            return {"success": True, "data": {"appointment": appointment}}
        elif action == "update":
            if date:
                appointment["date"] = date
            if time:
                appointment["time"] = time
            return {"success": True, "message": "Appointment updated.", "data": {"appointment": appointment}}
        elif action == "cancel":
            appointment["status"] = "cancelled"
            return {"success": True, "message": "Appointment cancelled.", "data": {"appointment": appointment}}
        else:
            return {"success": False, "message": "Invalid action."}

    def access_user_info(self):
        return {"success": True, "data": {"user_info": self.user_info}}

    def access_medical_history(self):
        return {"success": True, "data": {"medical_history": self.medical_history}}

    def request_prescription(self, *, medication_name, dosage, doctor_id):
        doctor = next((d for d in self.doctors if d["id"] == doctor_id), None)
        if not doctor:
            return {"success": False, "message": "Doctor not found."}
        prescription_id = f"rx{len(self.prescriptions)+1}"
        prescription = {
            "id": prescription_id,
            "medication_name": medication_name,
            "dosage": dosage,
            "doctor_id": doctor_id,
            "status": "requested"
        }
        self.prescriptions.append(prescription)
        return {"success": True, "data": {"prescription_id": prescription_id}}

    def view_prescriptions(self):
        return {"success": True, "data": {"prescriptions": self.prescriptions}}

    def send_message(self, *, consultation_id, message_content):
        consultation = next((c for c in self.consultations if c["id"] == consultation_id), None)
        if not consultation:
            return {"success": False, "message": "Consultation not found."}
        message = {"from": "user", "content": message_content}
        consultation["messages"].append(message)
        doctor_response = {"from": "doctor", "content": "Thank you for your message. I will respond shortly."}
        consultation["messages"].append(doctor_response)
        return {"success": True, "data": {"doctor_response": doctor_response["content"]}}

    def leave_review(self, *, doctor_id, rating, review_content):
        doctor = next((d for d in self.doctors if d["id"] == doctor_id), None)
        if not doctor:
            return {"success": False, "message": "Doctor not found."}
        if not (1 <= rating <= 5):
            return {"success": False, "message": "Rating must be between 1 and 5."}
        review = {
            "doctor_id": doctor_id,
            "rating": rating,
            "review_content": review_content
        }
        self.reviews.append(review)
        return {"success": True, "message": "Review submitted."}

    def view_reviews(self, *, doctor_id):
        doctor_reviews = [r for r in self.reviews if r["doctor_id"] == doctor_id]
        return {"success": True, "data": {"reviews": doctor_reviews}}