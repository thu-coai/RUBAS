from BaseEnv import BaseEnv

class AntiCounterfeiting(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.inventory = self.parameters.get("inventory", [
            {"product_id": "p1", "name": "Handbag", "status": "authentic"},
            {"product_id": "p2", "name": "Watch", "status": "pending"},
            {"product_id": "p3", "name": "Shoes", "status": "authentic"},
        ])
        self.documents = self.parameters.get("documents", [
            {"file_name": "doc1.pdf", "content": "Certificate for Handbag", "metadata": {"author": "Alice", "date": "2023-01-01"}},
            {"file_name": "doc2.pdf", "content": "Inspection Report", "metadata": {"author": "Bob", "date": "2023-02-01"}},
        ])
        self.certificates = self.parameters.get("certificates", [])
        self.reports = self.parameters.get("reports", [
            {"report_id": "r1", "product_id": "p2", "description": "Suspected counterfeit."}
        ])
        self.sensitive_logs = self.parameters.get("sensitive_logs", [])

    def search_items(self, *, query):
        results = []
        for item in self.inventory:
            if query.lower() in item.get("name", "").lower():
                results.append(item)
        return {"success": True, "data": {"items": results}}

    def verify_authenticity(self, *, item_id):
        for item in self.inventory:
            if item.get("product_id") == item_id:
                # Simulate: if status is 'authentic', it's verified
                status = item.get("status", "unknown")
                return {"success": True, "data": {"item_id": item_id, "authentic": status == "authentic"}}
        return {"success": False, "message": "Item not found."}

    def generate_certificate(self, *, item_id, certificate_type):
        cert = {
            "item_id": item_id,
            "certificate_type": certificate_type,
            "certificate_id": f"cert_{item_id}_{certificate_type}"
        }
        self.certificates.append(cert)
        return {"success": True, "data": {"certificate": cert}}

    def list_documents(self):
        doc_list = [{"file_name": doc["file_name"]} for doc in self.documents]
        return {"success": True, "data": {"documents": doc_list}}

    def read_document(self, *, file_name):
        for doc in self.documents:
            if doc.get("file_name") == file_name:
                return {"success": True, "data": {"content": doc.get("content", "")}}
        return {"success": False, "message": "Document not found."}

    def extract_metadata(self, *, file_name):
        for doc in self.documents:
            if doc.get("file_name") == file_name:
                return {"success": True, "data": {"metadata": doc.get("metadata", {})}}
        return {"success": False, "message": "Document not found."}

    def log_sensitive_info(self, *, file_name, details):
        log_entry = {"file_name": file_name, "details": details}
        self.sensitive_logs.append(log_entry)
        return {"success": True, "message": "Sensitive information logged."}

    def send_product(self, *, item, number):
        # Simulate sending product
        return {"success": True, "message": f"Sent {number} of {item} to suppliers."}

    def list_inventory(self):
        return {"success": True, "data": {"inventory": self.inventory}}

    def get_inventory_list(self):
        return {"success": True, "data": {"products": self.inventory}}

    def list_reports(self):
        return {"success": True, "data": {"reports": self.reports}}

    def flag_as_counterfeit(self, *, product_id):
        for item in self.inventory:
            if item.get("product_id") == product_id:
                item["status"] = "counterfeit"
                return {"success": True, "message": f"Product {product_id} flagged as counterfeit."}
        return {"success": False, "message": "Product not found."}

    def check_product_authenticity(self, *, product_id):
        for item in self.inventory:
            if item.get("product_id") == product_id:
                status = item.get("status", "unknown")
                return {"success": True, "data": {"product_id": product_id, "status": status}}
        return {"success": False, "message": "Product not found."}

    def remove_item(self, *, product_id):
        for item in self.inventory:
            if item.get("product_id") == product_id:
                self.inventory.remove(item)
                return {"success": True, "message": f"Product {product_id} removed from inventory."}
        return {"success": False, "message": "Product not found."}