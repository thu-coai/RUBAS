from BaseEnv import BaseEnv

class CloudSecurity(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.policies = self.parameters.get("policies", [])
        self.logs = self.parameters.get("logs", [])
        self.blocked_domains = set(self.parameters.get("blocked_domains", []))
        self.policy_counter = 1

    def create_policy(self, *, policy_name, policy_type, domains=None):
        if policy_type not in ["whitelist", "blacklist"]:
            return {"success": False, "message": "Invalid policy_type."}
        if domains is None:
            domains = []
        policy_id = f"policy_{self.policy_counter}"
        self.policy_counter += 1
        policy = {
            "id": policy_id,
            "name": policy_name,
            "type": policy_type,
            "domains": list(domains)
        }
        self.policies.append(policy)
        return {"success": True, "data": {"policy_id": policy_id}}

    def update_policy(self, *, policy_id, policy_name, policy_type, domains):
        if policy_type not in ["whitelist", "blacklist"]:
            return {"success": False, "message": "Invalid policy_type."}
        for policy in self.policies:
            if policy["id"] == policy_id:
                policy["name"] = policy_name
                policy["type"] = policy_type
                policy["domains"] = list(domains)
                return {"success": True, "message": "Policy updated."}
        return {"success": False, "message": "Policy not found."}

    def get_log_details(self, *, log_id):
        for log in self.logs:
            if log.get("id") == log_id:
                return {"success": True, "data": log}
        return {"success": False, "message": "Log not found."}

    def unblock_domains(self, *, domains):
        removed = []
        for domain in domains:
            if domain in self.blocked_domains:
                self.blocked_domains.remove(domain)
                removed.append(domain)
        return {"success": True, "data": {"unblocked_domains": removed}}

    def block_domains(self, *, domains):
        added = []
        for domain in domains:
            if domain not in self.blocked_domains:
                self.blocked_domains.add(domain)
                added.append(domain)
        return {"success": True, "data": {"blocked_domains": added}}