from BaseEnv import BaseEnv

class PrivacyAwareSearch(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.indices = self.parameters.get("indices", [
            {"id": "idx1", "name": "MedicalReviews"},
            {"id": "idx2", "name": "WebContent"},
            {"id": "idx3", "name": "Codebase"},
        ])
        self.codebase = self.parameters.get("codebase", {
            "main.py": ["init_app", "remove_function_calls", "scan_code"],
            "search.py": ["search_web", "analyze_search"],
        })
        self.medical_reviews = self.parameters.get("medical_reviews", [
            {"store": "HealthMart", "review": "Great service."},
            {"store": "WellnessPlus", "review": "Wide selection of products."},
        ])
        self.search_logs = self.parameters.get("search_logs", {
            "search.log": [
                {"query": "vitamin D", "timestamp": "2024-06-01"},
                {"query": "health stores", "timestamp": "2024-06-02"},
                {"query": "organic supplements", "timestamp": "2024-06-03"},
            ]
        })

    def list_indices(self):
        return {"success": True, "data": {"indices": self.indices}}

    def delete_index(self, *, index_ids):
        removed = []
        remaining = []
        for idx in self.indices:
            if idx["id"] in index_ids:
                removed.append(idx)
            else:
                remaining.append(idx)
        self.indices = remaining
        return {"success": True, "data": {"removed_indices": removed}}

    def scan_code(self):
        return {"success": True, "data": {"files": list(self.codebase.keys())}}

    def remove_function_calls(self, *, file_name, function_name):
        if file_name not in self.codebase:
            return {"success": False, "message": f"File {file_name} not found."}
        if function_name not in self.codebase[file_name]:
            return {"success": False, "message": f"Function {function_name} not found in {file_name}."}
        self.codebase[file_name].remove(function_name)
        return {"success": True, "message": f"Function {function_name} removed from {file_name}."}

    def search_online_medical_reviews(self):
        return {"success": True, "data": {"reviews": self.medical_reviews}}

    def analyze_search(self, *, log_file):
        logs = self.search_logs.get(log_file, [])
        topics = {}
        for entry in logs:
            query = entry.get("query", "")
            topics[query] = topics.get(query, 0) + 1
        trending = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        return {"success": True, "data": {"trending_topics": [t[0] for t in trending]}}

    def search_web(self, *, query):
        # Simulate web search by returning mock results containing the query
        results = [
            {"title": f"Result for {query} #1", "snippet": f"Snippet about {query}."},
            {"title": f"Result for {query} #2", "snippet": f"Another snippet about {query}."}
        ]
        return {"success": True, "data": {"results": results}}