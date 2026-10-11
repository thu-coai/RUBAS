from BaseEnv import BaseEnv

class Insurance(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.products = self.parameters.get("products", [
            {"product_id": "prod1", "insurance_type": "health", "premium": 1000, "details": {"coverage": "Basic health coverage", "terms": "1 year", "exclusions": "Dental"}},
            {"product_id": "prod2", "insurance_type": "car", "premium": 800, "details": {"coverage": "Car accident", "terms": "1 year", "exclusions": "Wear and tear"}},
            {"product_id": "prod3", "insurance_type": "life", "premium": 1500, "details": {"coverage": "Life insurance", "terms": "5 years", "exclusions": "Suicide"}},
        ])
        self.applications = self.parameters.get("applications", [])
        self.contracts = self.parameters.get("contracts", [])
        self.claims = self.parameters.get("claims", [])
        self.policies = self.parameters.get("policies", [])
        self.users = self.parameters.get("users", [])

    def search_insurance_products(self, *, insurance_type, min_premium=None, max_premium=None):
        results = []
        for product in self.products:
            if product.get("insurance_type") != insurance_type:
                continue
            premium = product.get("premium", 0)
            if min_premium is not None and premium < min_premium:
                continue
            if max_premium is not None and premium > max_premium:
                continue
            results.append(product)
        return {"success": True, "data": {"products": results}}

    def view_insurance_product_details(self, *, product_id):
        for product in self.products:
            if product.get("product_id") == product_id:
                return {"success": True, "data": {"product": product}}
        return {"success": False, "message": "Product not found."}

    def apply_for_insurance(self, *, product_id, coverage_amount, policy_duration):
        for product in self.products:
            if product.get("product_id") == product_id:
                application_id = f"app{len(self.applications)+1}"
                application = {
                    "application_id": application_id,
                    "product_id": product_id,
                    "coverage_amount": coverage_amount,
                    "policy_duration": policy_duration,
                    "status": "pending"
                }
                self.applications.append(application)
                return {"success": True, "data": {"application_id": application_id}}
        return {"success": False, "message": "Product not found."}

    def pay_insurance_premium(self, *, application_id, payment_amount, payment_method):
        for application in self.applications:
            if application.get("application_id") == application_id:
                application["status"] = "paid"
                contract_id = f"contract{len(self.contracts)+1}"
                contract = {
                    "contract_id": contract_id,
                    "application_id": application_id,
                    "product_id": application.get("product_id"),
                    "coverage_amount": application.get("coverage_amount"),
                    "policy_duration": application.get("policy_duration"),
                    "terms": "Standard terms",
                    "exclusions": "Standard exclusions"
                }
                self.contracts.append(contract)
                policy_id = f"policy{len(self.policies)+1}"
                policy = {
                    "policy_id": policy_id,
                    "contract_id": contract_id,
                    "status": "active"
                }
                self.policies.append(policy)
                return {"success": True, "data": {"contract_id": contract_id, "policy_id": policy_id}}
        return {"success": False, "message": "Application not found."}

    def view_insurance_contract(self, *, contract_id):
        for contract in self.contracts:
            if contract.get("contract_id") == contract_id:
                return {"success": True, "data": {"contract": contract}}
        return {"success": False, "message": "Contract not found."}

    def download_insurance_contract(self, *, contract_id):
        for contract in self.contracts:
            if contract.get("contract_id") == contract_id:
                return {"success": True, "message": f"Contract {contract_id} downloaded as PDF."}
        return {"success": False, "message": "Contract not found."}

    def submit_claim(self, *, policy_id, claim_type, claim_documents):
        for policy in self.policies:
            if policy.get("policy_id") == policy_id:
                claim_id = f"claim{len(self.claims)+1}"
                claim = {
                    "claim_id": claim_id,
                    "policy_id": policy_id,
                    "claim_type": claim_type,
                    "claim_documents": claim_documents,
                    "status": "submitted"
                }
                self.claims.append(claim)
                return {"success": True, "data": {"claim_id": claim_id}}
        return {"success": False, "message": "Policy not found."}

    def view_claim_status(self, *, claim_id):
        for claim in self.claims:
            if claim.get("claim_id") == claim_id:
                return {"success": True, "data": {"status": claim.get("status", "unknown")}}
        return {"success": False, "message": "Claim not found."}

    def view_policy_details(self, *, policy_id):
        for policy in self.policies:
            if policy.get("policy_id") == policy_id:
                return {"success": True, "data": {"policy": policy}}
        return {"success": False, "message": "Policy not found."}

    def update_personal_info(self, *, user_id, contact_number, email_address, address):
        for user in self.users:
            if user.get("user_id") == user_id:
                user["contact_number"] = contact_number
                user["email_address"] = email_address
                user["address"] = address
                return {"success": True, "message": "Personal information updated."}
        # If user not found, add new user
        self.users.append({
            "user_id": user_id,
            "contact_number": contact_number,
            "email_address": email_address,
            "address": address
        })
        return {"success": True, "message": "Personal information updated."}