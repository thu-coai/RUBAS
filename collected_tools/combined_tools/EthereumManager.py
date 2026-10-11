from BaseEnv import BaseEnv

class EthereumManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.accounts = self.parameters.get("accounts", [])
        self.contracts = self.parameters.get("contracts", [])
        self.transactions = self.parameters.get("transactions", [])
        self.next_account_id = 1
        self.next_contract_address = 1
        self.next_tx_hash = 1

    def deploy_smart_contract(self, *, contract_bytecode, constructor_args, gas_limit=None):
        contract_address = f"0xCONTRACT{self.next_contract_address:04d}"
        self.next_contract_address += 1
        contract = {
            "address": contract_address,
            "bytecode": contract_bytecode,
            "constructor_args": constructor_args,
            "gas_limit": gas_limit,
            "functions": {},
        }
        self.contracts.append(contract)
        return {
            "success": True,
            "data": {
                "contract_address": contract_address,
                "contract": contract
            }
        }

    def call_smart_contract_function(self, *, contract_address, function_name, function_args, value="0", gas_limit=None):
        contract = next((c for c in self.contracts if c["address"] == contract_address), None)
        if not contract:
            return {"success": False, "message": "Contract address not found."}
        tx_hash = f"0xTX{self.next_tx_hash:06d}"
        self.next_tx_hash += 1
        tx = {
            "hash": tx_hash,
            "contract_address": contract_address,
            "function_name": function_name,
            "function_args": function_args,
            "value": value,
            "gas_limit": gas_limit
        }
        self.transactions.append(tx)
        return {
            "success": True,
            "data": {
                "transaction_hash": tx_hash,
                "result": f"Simulated call to {function_name} on {contract_address}"
            }
        }

    def transfer_ether(self, *, from_address, to_address, amount_ether, gas_limit=None):
        from_account = next((a for a in self.accounts if a["address"] == from_address), None)
        to_account = next((a for a in self.accounts if a["address"] == to_address), None)
        if not from_account or not to_account:
            return {"success": False, "message": "Sender or recipient address not found."}
        if from_account.get("balance", 0) < amount_ether:
            return {"success": False, "message": "Insufficient balance."}
        from_account["balance"] -= amount_ether
        to_account["balance"] += amount_ether
        tx_hash = f"0xTX{self.next_tx_hash:06d}"
        self.next_tx_hash += 1
        tx = {
            "hash": tx_hash,
            "from": from_address,
            "to": to_address,
            "amount_ether": amount_ether,
            "gas_limit": gas_limit
        }
        self.transactions.append(tx)
        return {
            "success": True,
            "data": {
                "transaction_hash": tx_hash,
                "from": from_address,
                "to": to_address,
                "amount_ether": amount_ether
            }
        }

    def create_ethereum_account(self):
        address = f"0xACCOUNT{self.next_account_id:04d}"
        private_key = f"PRIVATEKEY{self.next_account_id:04d}"
        self.next_account_id += 1
        account = {
            "address": address,
            "private_key": private_key,
            "balance": 0
        }
        self.accounts.append(account)
        return {
            "success": True,
            "data": {
                "account": account
            }
        }

    def import_ethereum_account(self, *, private_key):
        address = f"0xIMPORTED{self.next_account_id:04d}"
        self.next_account_id += 1
        account = {
            "address": address,
            "private_key": private_key,
            "balance": 0
        }
        self.accounts.append(account)
        return {
            "success": True,
            "data": {
                "account": account
            }
        }

    def estimate_gas_cost(self, *, contract_address, function_name, function_args):
        contract = next((c for c in self.contracts if c["address"] == contract_address), None)
        if not contract:
            return {"success": False, "message": "Contract address not found."}
        estimated_gas = 21000 + 1000 * len(function_args)
        return {
            "success": True,
            "data": {
                "estimated_gas": estimated_gas
            }
        }

    def compile_solidity(self, *, contract_code):
        bytecode = f"MOCK_BYTECODE_{hash(contract_code) % 100000}"
        return {
            "success": True,
            "data": {
                "bytecode": bytecode
            }
        }

    def sign_message(self, *, message, private_key):
        signature = f"SIG_{hash(message + private_key) % 100000}"
        return {
            "success": True,
            "data": {
                "signature": signature
            }
        }

    def verify_message(self, *, message, signature, account_address):
        account = next((a for a in self.accounts if a["address"] == account_address), None)
        if not account:
            return {"success": False, "message": "Account address not found."}
        expected_signature = f"SIG_{hash(message + account['private_key']) % 100000}"
        verified = signature == expected_signature
        return {
            "success": True,
            "data": {
                "verified": verified
            }
        }

    def query_ethereum_data(self, *, query_type, query_value):
        if query_type == "addresses":
            res = []
            for account in self.accounts:
                if query_value in account["address"]:
                    res.append(account["address"])
            for contract in self.contracts:
                if query_value in contract["address"]:
                    res.append(contract["address"])
            return {
                "success": True,
                "data": {
                    "addresses": res
                }
            }
        elif query_type == "address info":
            account = next((a for a in self.accounts if a["address"] == query_value), None)
            if account:
                return {
                    "success": True,
                    "data": {
                        "address_info": account
                    }
                }
            contract = next((c for c in self.contracts if c["address"] == query_value), None)
            if contract:
                return {
                    "success": True,
                    "data": {
                        "address_info": contract
                    }
                }
            return {"success": False, "message": "Address not found."}
        elif query_type == "transaction hash":
            tx = next((t for t in self.transactions if t["hash"] == query_value), None)
            if tx:
                return {
                    "success": True,
                    "data": {
                        "transaction": tx
                    }
                }
            return {"success": False, "message": "Transaction hash not found."}
        else:
            return {"success": False, "message": "Invalid query_type."}