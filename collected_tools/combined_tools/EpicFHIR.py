from BaseEnv import BaseEnv

class EpicFHIR(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.patients = self.parameters.get("patients", [])
        self.doctors = self.parameters.get("doctors", [])
        self.clinical_documents = self.parameters.get("clinical_documents", {})
        self.appointments = self.parameters.get("appointments", {})
        self.patient_records = self.parameters.get("patient_records", {})
        self.diagnostic_reports = self.parameters.get("diagnostic_reports", {})
        self.files = self.parameters.get("files", {})

    def search_patients(self, *, search_term, max_results=10):
        results = []
        for patient in self.patients:
            if (
                search_term.lower() in str(patient.get("id", "")).lower()
                or search_term.lower() in str(patient.get("name", "")).lower()
                or search_term.lower() in str(patient.get("demographics", "")).lower()
                or search_term.lower() in str(patient.get("disease", "")).lower()
            ):
                results.append(patient)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"patients": results}}

    def get_patient_details(self, *, patient_id):
        for patient in self.patients:
            if patient.get("id", "") == patient_id:
                return {"success": True, "data": patient}
        return {"success": False, "message": "Patient not found."}

    def search_doctors(self, *, search_term, max_results=10):
        results = []
        for doctor in self.doctors:
            if (
                search_term.lower() in str(doctor.get("id", "")).lower()
                or search_term.lower() in str(doctor.get("name", "")).lower()
                or search_term.lower() in str(doctor.get("specialty", "")).lower()
            ):
                results.append(doctor)
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"doctors": results}}

    def manage_clinical_documents(
        self,
        *,
        patient_id,
        action,
        document_id=None,
        document_data=None,
        max_results=10
    ):
        if patient_id not in self.clinical_documents:
            self.clinical_documents[patient_id] = []
        docs = self.clinical_documents[patient_id]
        if action == "list":
            return {
                "success": True,
                "data": {"documents": docs[:max_results]},
            }
        elif action == "create":
            if not document_data:
                return {"success": False, "message": "Missing document_data for create."}
            new_id = f"doc_{len(docs)+1}"
            doc = {"id": new_id}
            doc.update(document_data)
            docs.append(doc)
            self.files[new_id] = doc
            return {"success": True, "data": {"document_id": new_id}}
        elif action == "update":
            if not document_id or not document_data:
                return {"success": False, "message": "Missing document_id or document_data for update."}
            for doc in docs:
                if doc.get("id") == document_id:
                    doc.update(document_data)
                    self.files[document_id] = doc
                    return {"success": True, "message": "Document updated."}
            return {"success": False, "message": "Document not found."}
        elif action == "delete":
            if not document_id:
                return {"success": False, "message": "Missing document_id for delete."}
            for i, doc in enumerate(docs):
                if doc.get("id") == document_id:
                    docs.pop(i)
                    self.files.pop(document_id, None)
                    return {"success": True, "message": "Document deleted."}
            return {"success": False, "message": "Document not found."}
        else:
            return {"success": False, "message": "Invalid action."}

    def manage_appointments(
        self,
        *,
        patient_id,
        action,
        appointment_id=None,
        appointment_data=None,
        max_results=10
    ):
        if patient_id not in self.appointments:
            self.appointments[patient_id] = []
        appts = self.appointments[patient_id]
        if action == "list":
            return {
                "success": True,
                "data": {"appointments": appts[:max_results]},
            }
        elif action == "create":
            if not appointment_data:
                return {"success": False, "message": "Missing appointment_data for create."}
            new_id = f"appt_{len(appts)+1}"
            appt = {"id": new_id}
            appt.update(appointment_data)
            appts.append(appt)
            self.files[new_id] = appt
            return {"success": True, "data": {"appointment_id": new_id}}
        elif action == "update":
            if not appointment_id or not appointment_data:
                return {"success": False, "message": "Missing appointment_id or appointment_data for update."}
            for appt in appts:
                if appt.get("id") == appointment_id:
                    appt.update(appointment_data)
                    self.files[appointment_id] = appt
                    return {"success": True, "message": "Appointment updated."}
            return {"success": False, "message": "Appointment not found."}
        elif action == "delete":
            if not appointment_id:
                return {"success": False, "message": "Missing appointment_id for delete."}
            for i, appt in enumerate(appts):
                if appt.get("id") == appointment_id:
                    appts.pop(i)
                    self.files.pop(appointment_id, None)
                    return {"success": True, "message": "Appointment deleted."}
            return {"success": False, "message": "Appointment not found."}
        else:
            return {"success": False, "message": "Invalid action."}

    def manage_patient_records(
        self,
        *,
        patient_id,
        action,
        record_data=None,
        max_results=10
    ):
        if patient_id not in self.patient_records:
            self.patient_records[patient_id] = []
        records = self.patient_records[patient_id]
        if action == "list":
            return {
                "success": True,
                "data": {"records": records[:max_results]},
            }
        elif action == "create":
            if not record_data:
                return {"success": False, "message": "Missing record_data for create."}
            new_id = f"rec_{len(records)+1}"
            rec = {"id": new_id}
            rec.update(record_data)
            records.append(rec)
            self.files[new_id] = rec
            return {"success": True, "data": {"record_id": new_id}}
        elif action == "update":
            if not record_data or not record_data.get("id"):
                return {"success": False, "message": "Missing record_data with id for update."}
            for rec in records:
                if rec.get("id") == record_data.get("id"):
                    rec.update(record_data)
                    self.files[rec.get("id")] = rec
                    return {"success": True, "message": "Record updated."}
            return {"success": False, "message": "Record not found."}
        elif action == "delete":
            if not record_data or not record_data.get("id"):
                return {"success": False, "message": "Missing record_data with id for delete."}
            for i, rec in enumerate(records):
                if rec.get("id") == record_data.get("id"):
                    records.pop(i)
                    self.files.pop(rec.get("id"), None)
                    return {"success": True, "message": "Record deleted."}
            return {"success": False, "message": "Record not found."}
        else:
            return {"success": False, "message": "Invalid action."}

    def manage_diagnostic_reports(
        self,
        *,
        patient_id,
        action,
        report_id=None,
        report_data=None,
        max_results=10
    ):
        if patient_id not in self.diagnostic_reports:
            self.diagnostic_reports[patient_id] = []
        reports = self.diagnostic_reports[patient_id]
        if action == "list":
            return {
                "success": True,
                "data": {"reports": reports[:max_results]},
            }
        elif action == "create":
            if not report_data:
                return {"success": False, "message": "Missing report_data for create."}
            new_id = f"rep_{len(reports)+1}"
            rep = {"id": new_id}
            rep.update(report_data)
            reports.append(rep)
            self.files[new_id] = rep
            return {"success": True, "data": {"report_id": new_id}}
        elif action == "update":
            if not report_id or not report_data:
                return {"success": False, "message": "Missing report_id or report_data for update."}
            for rep in reports:
                if rep.get("id") == report_id:
                    rep.update(report_data)
                    self.files[report_id] = rep
                    return {"success": True, "message": "Report updated."}
            return {"success": False, "message": "Report not found."}
        elif action == "delete":
            if not report_id:
                return {"success": False, "message": "Missing report_id for delete."}
            for i, rep in enumerate(reports):
                if rep.get("id") == report_id:
                    reports.pop(i)
                    self.files.pop(report_id, None)
                    return {"success": True, "message": "Report deleted."}
            return {"success": False, "message": "Report not found."}
        else:
            return {"success": False, "message": "Invalid action."}

    def download_files(self, *, file_ids):
        found = []
        not_found = []
        for fid in file_ids:
            if fid in self.files:
                found.append(self.files[fid])
            else:
                not_found.append(fid)
        return {
            "success": True,
            "data": {"files": found},
            "not_found": not_found,
        }