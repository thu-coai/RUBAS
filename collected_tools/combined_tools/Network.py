from BaseEnv import BaseEnv

class Network(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.packets = self.parameters.get("packets", [
            {"name": "packet1", "data": "mock_data_1"},
            {"name": "packet2", "data": "mock_data_2"},
            {"name": "packet3", "data": "mock_data_3"},
        ])
        self.sent_emails = []
        self.doctors = self.parameters.get("doctors", [
            {"name": "Dr. Alice Smith", "email": "alice.smith@hospital.org", "phone": "555-1234"},
            {"name": "Dr. Bob Jones", "email": "bob.jones@hospital.org", "phone": "555-5678"},
        ])
        self.subscribers = self.parameters.get("subscribers", [
            "subscriber1@example.com",
            "subscriber2@example.com",
        ])
        self.sent_newsletters = []

    def sniff_traffic_packets(self):
        return {"success": True, "data": {"packets": self.packets}}

    def analyze_traffic_packets(self, *, packet_names):
        if not isinstance(packet_names, list):
            return {"success": False, "message": "packet_names must be a list."}
        found_packets = [p for p in self.packets if p["name"] in packet_names]
        analysis = []
        for packet in found_packets:
            analysis.append({
                "name": packet["name"],
                "analysis": f"Simulated analysis for {packet['name']}"
            })
        return {"success": True, "data": {"analysis": analysis}}

    def email_content(self, *, email_address, content):
        if not isinstance(email_address, str) or not isinstance(content, str):
            return {"success": False, "message": "Invalid email_address or content type."}
        self.sent_emails.append({"to": email_address, "content": content})
        return {"success": True, "message": f"Email sent to {email_address}."}

    def lookup_doctor_contacts(self, *, name):
        if not isinstance(name, str):
            return {"success": False, "message": "Invalid name type."}
        matches = [doc for doc in self.doctors if doc["name"].lower() == name.lower()]
        if matches:
            return {"success": True, "data": {"contacts": matches}}
        else:
            return {"success": True, "data": {"contacts": []}}

    def send_newsletter(self, *, subject, content):
        if not isinstance(subject, str) or not isinstance(content, str):
            return {"success": False, "message": "Invalid subject or content type."}
        newsletter = {"subject": subject, "content": content, "recipients": self.subscribers}
        self.sent_newsletters.append(newsletter)
        return {"success": True, "message": f"Newsletter sent to {len(self.subscribers)} subscribers."}