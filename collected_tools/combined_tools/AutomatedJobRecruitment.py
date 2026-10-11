from BaseEnv import BaseEnv

class AutomatedJobRecruitment(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.applications = self.parameters.get("applications", [])
        self.documents = self.parameters.get("documents", {})
        self.reports = self.parameters.get("reports", [])
        self.jobs = self.parameters.get("jobs", [])
        self.job_postings = self.parameters.get("job_postings", [])
        self.positions = self.parameters.get("positions", [])
        self.applicants = self.parameters.get("applicants", [])
        self.selected_candidates = self.parameters.get("selected_candidates", [])
        self.portal = {
            "online": True,
            "version": self.parameters.get("portal_version", "v1.0.0")
        }

    def access_applications(self):
        return {"success": True, "data": {"applications": self.applications}}

    def read_document(self, *, file_name):
        content = self.documents.get(file_name)
        if content is None:
            return {"success": False, "message": "Document not found."}
        return {"success": True, "data": {"content": content}}

    def publish_report(self, *, content):
        self.reports.append(content)
        return {"success": True, "message": "Report published."}

    def send_out_job(self, *, candidates_list, job_title):
        job = next((j for j in self.jobs if j.get("title") == job_title), None)
        if job is None:
            return {"success": False, "message": "Job title not found."}
        for candidate in candidates_list:
            job.setdefault("sent_to", []).append(candidate)
        return {"success": True, "message": "Job sent to candidates."}

    def retrieve_job(self, *, job_title):
        job = next((j for j in self.jobs if j.get("title") == job_title), None)
        if job is None:
            return {"success": False, "message": "Job not found."}
        return {"success": True, "data": {"job": job}}

    def update_job(self, *, job_title, job_description):
        job = next((j for j in self.jobs if j.get("title") == job_title), None)
        if job is None:
            return {"success": False, "message": "Job not found."}
        job["description"] = job_description
        return {"success": True, "message": "Job updated."}

    def list_jobs(self):
        return {"success": True, "data": {"jobs": self.jobs}}

    def remove_job(self, *, job_id):
        job = next((j for j in self.jobs if j.get("id") == job_id), None)
        if job is None:
            return {"success": False, "message": "Job not found."}
        self.jobs.remove(job)
        return {"success": True, "message": "Job removed."}

    def portal_status(self):
        return {"success": True, "data": {"online": self.portal["online"], "version": self.portal["version"]}}

    def update_portal(self, *, version):
        self.portal["version"] = version
        return {"success": True, "message": f"Portal updated to version {version}."}

    def get_job_requirements(self):
        requirements = [pos.get("requirements", "") for pos in self.positions]
        return {"success": True, "data": {"requirements": requirements}}

    def apply_filter(self, *, criterion):
        filtered = [a for a in self.applicants if criterion.lower() in str(a).lower()]
        return {"success": True, "data": {"filtered_applicants": filtered}}

    def list_job_postings(self):
        return {"success": True, "data": {"job_postings": self.job_postings}}

    def deactivate_job_posting(self, *, job_id):
        posting = next((jp for jp in self.job_postings if jp.get("id") == job_id), None)
        if posting is None:
            return {"success": False, "message": "Job posting not found."}
        posting["active"] = False
        return {"success": True, "message": "Job posting deactivated."}

    def list_positions(self):
        return {"success": True, "data": {"positions": self.positions}}

    def list_applicants(self):
        return {"success": True, "data": {"applicants": self.applicants}}

    def select_candidate(self, *, applicant_name, position_title):
        applicant = next((a for a in self.applicants if a.get("name") == applicant_name), None)
        position = next((p for p in self.positions if p.get("title") == position_title), None)
        if applicant is None or position is None:
            return {"success": False, "message": "Applicant or position not found."}
        self.selected_candidates.append({"applicant": applicant_name, "position": position_title})
        return {"success": True, "message": "Candidate selected for position."}