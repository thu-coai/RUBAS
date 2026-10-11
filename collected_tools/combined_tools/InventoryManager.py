from BaseEnv import BaseEnv

class InventoryManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.items = self.parameters.get("items", [])
        self.suppliers = self.parameters.get("suppliers", [])
        self.categories = self.parameters.get("categories", [])
        self.alerts = self.parameters.get("alerts", [])
        self._item_id_counter = 1
        self._alert_id_counter = 1

    def add_item(self, *, item_name, category, quantity, supplier=None, description=None):
        if not isinstance(item_name, str) or not item_name.strip():
            return {"success": False, "message": "item_name must be a non-empty string."}
        if not isinstance(category, str) or not category.strip():
            return {"success": False, "message": "category must be a non-empty string."}
        if not isinstance(quantity, int) or quantity <= 0:
            return {"success": False, "message": "quantity must be a positive integer."}
        if supplier is not None and (not isinstance(supplier, str) or not supplier.strip()):
            return {"success": False, "message": "supplier must be a non-empty string if provided."}
        if description is not None and (not isinstance(description, str) or not description.strip()):
            return {"success": False, "message": "description must be a non-empty string if provided."}
        item_id = f"item_{self._item_id_counter}"
        self._item_id_counter += 1
        item = {
            "item_id": item_id,
            "item_name": item_name,
            "category": category,
            "quantity": quantity,
            "supplier": supplier,
            "description": description,
        }
        self.items.append(item)
        if category not in self.categories:
            self.categories.append(category)
        if supplier and supplier not in self.suppliers:
            self.suppliers.append(supplier)
        return {"success": True, "data": {"item_id": item_id}}

    def update_item(self, *, item_id, item_name=None, category=None, quantity=None, supplier=None, description=None):
        if not isinstance(item_id, str) or not item_id.strip():
            return {"success": False, "message": "item_id must be a non-empty string."}
        for item in self.items:
            if item.get("item_id") == item_id:
                if item_name is not None:
                    if not isinstance(item_name, str) or not item_name.strip():
                        return {"success": False, "message": "item_name must be a non-empty string if provided."}
                    item["item_name"] = item_name
                if category is not None:
                    if not isinstance(category, str) or not category.strip():
                        return {"success": False, "message": "category must be a non-empty string if provided."}
                    item["category"] = category
                    if category not in self.categories:
                        self.categories.append(category)
                if quantity is not None:
                    if not isinstance(quantity, int) or quantity <= 0:
                        return {"success": False, "message": "quantity must be a positive integer if provided."}
                    item["quantity"] = quantity
                if supplier is not None:
                    if not isinstance(supplier, str) or not supplier.strip():
                        return {"success": False, "message": "supplier must be a non-empty string if provided."}
                    item["supplier"] = supplier
                    if supplier not in self.suppliers:
                        self.suppliers.append(supplier)
                if description is not None:
                    if not isinstance(description, str) or not description.strip():
                        return {"success": False, "message": "description must be a non-empty string if provided."}
                    item["description"] = description
                return {"success": True, "message": "Item updated."}
        return {"success": False, "message": "Item not found."}

    def delete_item(self, *, item_id):
        if not isinstance(item_id, str) or not item_id.strip():
            return {"success": False, "message": "item_id must be a non-empty string."}
        for item in self.items:
            if item.get("item_id") == item_id:
                self.items.remove(item)
                return {"success": True, "message": "Item deleted."}
        return {"success": False, "message": "Item not found."}

    def search_items(self, *, keyword=None, category=None, page=1, results_per_page=10):
        results = self.items
        if keyword is not None and isinstance(keyword, str) and keyword.strip():
            results = [item for item in results if keyword.lower() in item.get("item_name", "").lower()]
        if category is not None and isinstance(category, str) and category.strip():
            results = [item for item in results if item.get("category", "") == category]
        if not isinstance(page, int) or page < 1:
            page = 1
        if not isinstance(results_per_page, int) or results_per_page < 1:
            results_per_page = 10
        start = (page - 1) * results_per_page
        end = start + results_per_page
        paged = results[start:end]
        return {"success": True, "data": {"items": paged, "total": len(results)}}

    def get_item_details(self, *, item_id):
        if not isinstance(item_id, str) or not item_id.strip():
            return {"success": False, "message": "item_id must be a non-empty string."}
        for item in self.items:
            if item.get("item_id") == item_id:
                return {"success": True, "data": {"item": item}}
        return {"success": False, "message": "Item not found."}

    def track_inventory(self, *, threshold):
        if not isinstance(threshold, int) or threshold <= 0:
            return {"success": False, "message": "threshold must be a positive integer."}
        low_stock = [item for item in self.items if item.get("quantity", 0) <= threshold]
        return {"success": True, "data": {"low_stock_items": low_stock}}

    def setup_alert(self, *, threshold, operation, alert_id=None, item_id=None, category=None):
        if not isinstance(threshold, int) or threshold <= 0:
            return {"success": False, "message": "threshold must be a positive integer."}
        if operation not in ["add", "update", "delete"]:
            return {"success": False, "message": "operation must be one of: add, update, delete."}
        if operation == "add":
            new_alert_id = alert_id if alert_id else f"alert_{self._alert_id_counter}"
            self._alert_id_counter += 1
            alert = {
                "alert_id": new_alert_id,
                "item_id": item_id,
                "category": category,
                "threshold": threshold,
            }
            self.alerts.append(alert)
            return {"success": True, "data": {"alert_id": new_alert_id}}
        elif operation == "update":
            for alert in self.alerts:
                if alert.get("alert_id") == alert_id:
                    alert["item_id"] = item_id
                    alert["category"] = category
                    alert["threshold"] = threshold
                    return {"success": True, "message": "Alert updated."}
            return {"success": False, "message": "Alert not found."}
        elif operation == "delete":
            for alert in self.alerts:
                if alert.get("alert_id") == alert_id:
                    self.alerts.remove(alert)
                    return {"success": True, "message": "Alert deleted."}
            return {"success": False, "message": "Alert not found."}
        return {"success": False, "message": "Invalid operation."}

    def search_suppliers(self, *, keyword=None, page=1, results_per_page=10):
        results = self.suppliers
        if keyword is not None and isinstance(keyword, str) and keyword.strip():
            results = [s for s in results if keyword.lower() in s.lower()]
        if not isinstance(page, int) or page < 1:
            page = 1
        if not isinstance(results_per_page, int) or results_per_page < 1:
            results_per_page = 10
        start = (page - 1) * results_per_page
        end = start + results_per_page
        paged = results[start:end]
        return {"success": True, "data": {"suppliers": paged, "total": len(results)}}

    def list_categories(self, *, page=1, results_per_page=10):
        results = self.categories
        if not isinstance(page, int) or page < 1:
            page = 1
        if not isinstance(results_per_page, int) or results_per_page < 1:
            results_per_page = 10
        start = (page - 1) * results_per_page
        end = start + results_per_page
        paged = results[start:end]
        return {"success": True, "data": {"categories": paged, "total": len(results)}}

    def update_inventory_cost(self, *, drug_name, new_cost):
        if not isinstance(drug_name, str) or not drug_name.strip():
            return {"success": False, "message": "drug_name must be a non-empty string."}
        if not (isinstance(new_cost, int) or isinstance(new_cost, float)):
            return {"success": False, "message": "new_cost must be a number."}
        updated = False
        for item in self.items:
            if item.get("item_name") == drug_name:
                item["cost"] = new_cost
                updated = True
        if updated:
            return {"success": True, "message": "Cost updated."}
        else:
            return {"success": False, "message": "Drug not found in inventory."}