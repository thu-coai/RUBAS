from BaseEnv import BaseEnv

class Dropbox(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        # files: {path: {"type": "file"/"folder", "name": ..., "content": ..., "metadata": {...}}}
        self.files = {
            "/MyDropbox/": {"type": "folder", "name": "MyDropbox", "content": [], "metadata": {}}
        }
        self.shared_links = {}  # {item_path: {"access_level": ..., "enabled": True/False}}
        self.shares = []  # [{"item_path": ..., "recipient_email": ..., "access_level": ...}]
        self.shared_files = {}  # {shared_file_id: {"name": ..., "content": ...}}
        # Optionally, pre-populate with parameters
        for f in self.parameters.get("files", []):
            path = f.get("path")
            if path:
                self.files[path] = f

    def upload_file(self, *, local_file_path, cloud_folder_path="/MyDropbox/"):
        if not isinstance(local_file_path, str) or not local_file_path:
            return {"success": False, "message": "Invalid local_file_path."}
        if cloud_folder_path not in self.files or self.files[cloud_folder_path]["type"] != "folder":
            return {"success": False, "message": "Destination folder does not exist."}
        file_name = local_file_path.split("/")[-1]
        file_path = cloud_folder_path.rstrip("/") + "/" + file_name
        if file_path in self.files:
            return {"success": False, "message": "File already exists at destination."}
        self.files[file_path] = {
            "type": "file",
            "name": file_name,
            "content": f"Simulated content of {local_file_path}",
            "metadata": {}
        }
        self.files[cloud_folder_path]["content"].append(file_path)
        return {"success": True, "message": f"File '{file_name}' uploaded to '{cloud_folder_path}'."}

    def download_file(self, *, user_cloud_file_path=None, shared_file_id=None, local_destination_folder="the default download folder of the local system"):
        if not user_cloud_file_path and not shared_file_id:
            return {"success": False, "message": "Either user_cloud_file_path or shared_file_id must be provided."}
        if user_cloud_file_path:
            file_entry = self.files.get(user_cloud_file_path)
            if not file_entry or file_entry["type"] != "file":
                return {"success": False, "message": "File not found in Dropbox."}
            file_name = file_entry["name"]
            return {"success": True, "message": f"File '{file_name}' downloaded to '{local_destination_folder}'."}
        if shared_file_id:
            shared_file = self.shared_files.get(shared_file_id)
            if not shared_file:
                return {"success": False, "message": "Shared file not found."}
            file_name = shared_file["name"]
            return {"success": True, "message": f"Shared file '{file_name}' downloaded to '{local_destination_folder}'."}
        return {"success": False, "message": "Invalid parameters."}

    def list_files_and_folders(self, *, cloud_folder_path="/MyDropbox/", max_results=10):
        folder = self.files.get(cloud_folder_path)
        if not folder or folder["type"] != "folder":
            return {"success": False, "message": "Folder not found."}
        items = []
        for path in folder["content"]:
            entry = self.files.get(path)
            if entry:
                items.append({"path": path, "type": entry["type"], "name": entry["name"]})
        return {"success": True, "data": {"items": items[:max_results]}}

    def create_folder(self, *, folder_name, parent_folder_path="/MyDropbox/"):
        if not folder_name or not isinstance(folder_name, str):
            return {"success": False, "message": "Invalid folder_name."}
        if parent_folder_path not in self.files or self.files[parent_folder_path]["type"] != "folder":
            return {"success": False, "message": "Parent folder does not exist."}
        new_folder_path = parent_folder_path.rstrip("/") + "/" + folder_name
        if new_folder_path in self.files:
            return {"success": False, "message": "Folder already exists."}
        self.files[new_folder_path] = {
            "type": "folder",
            "name": folder_name,
            "content": [],
            "metadata": {}
        }
        self.files[parent_folder_path]["content"].append(new_folder_path)
        return {"success": True, "message": f"Folder '{folder_name}' created in '{parent_folder_path}'."}

    def share_item(self, *, item_path, recipient_email, access_level):
        if item_path not in self.files:
            return {"success": False, "message": "Item not found."}
        if access_level not in ["view", "comment", "edit"]:
            return {"success": False, "message": "Invalid access_level."}
        self.shares.append({
            "item_path": item_path,
            "recipient_email": recipient_email,
            "access_level": access_level
        })
        return {"success": True, "message": f"Item '{item_path}' shared with {recipient_email} ({access_level})."}

    def delete_item(self, *, item_path):
        if item_path not in self.files:
            return {"success": False, "message": "Item not found."}
        entry = self.files[item_path]
        # Remove from parent folder's content
        parent_path = "/".join(item_path.rstrip("/").split("/")[:-1])
        if not parent_path:
            parent_path = "/"
        if parent_path in self.files and "content" in self.files[parent_path]:
            if item_path in self.files[parent_path]["content"]:
                self.files[parent_path]["content"].remove(item_path)
        # Remove all children if folder
        if entry["type"] == "folder":
            for child in list(entry["content"]):
                self.delete_item(item_path=child)
        del self.files[item_path]
        return {"success": True, "message": f"Item '{item_path}' deleted."}

    def search_items(self, *, query, max_results=50):
        results = []
        for path, entry in self.files.items():
            if query.lower() in entry["name"].lower() or query.lower() in path.lower():
                results.append({"path": path, "type": entry["type"], "name": entry["name"]})
            if len(results) >= max_results:
                break
        return {"success": True, "data": {"items": results}}

    def get_item_metadata(self, *, item_path):
        entry = self.files.get(item_path)
        if not entry:
            return {"success": False, "message": "Item not found."}
        return {"success": True, "data": {"metadata": entry.get("metadata", {})}}

    def move_item(self, *, item_path, destination_folder_path):
        if item_path not in self.files:
            return {"success": False, "message": "Item not found."}
        if destination_folder_path not in self.files or self.files[destination_folder_path]["type"] != "folder":
            return {"success": False, "message": "Destination folder does not exist."}
        entry = self.files[item_path]
        old_parent_path = "/".join(item_path.rstrip("/").split("/")[:-1])
        if not old_parent_path:
            old_parent_path = "/"
        if old_parent_path in self.files and "content" in self.files[old_parent_path]:
            if item_path in self.files[old_parent_path]["content"]:
                self.files[old_parent_path]["content"].remove(item_path)
        new_path = destination_folder_path.rstrip("/") + "/" + entry["name"]
        if new_path in self.files:
            return {"success": False, "message": "Item with same name exists in destination."}
        self.files[new_path] = entry
        self.files[destination_folder_path]["content"].append(new_path)
        del self.files[item_path]
        return {"success": True, "message": f"Item moved to '{destination_folder_path}' as '{new_path}'."}

    def create_link(self, *, item_path, access_level):
        if item_path not in self.files:
            return {"success": False, "message": "Item not found."}
        if access_level not in ["view", "comment", "edit"]:
            return {"success": False, "message": "Invalid access_level."}
        self.shared_links[item_path] = {"access_level": access_level, "enabled": True}
        link = f"https://dropbox.mock/{item_path.strip('/')}"
        return {"success": True, "data": {"link": link, "access_level": access_level}}

    def disable_link(self, *, item_path):
        if item_path not in self.shared_links or not self.shared_links[item_path]["enabled"]:
            return {"success": False, "message": "No active link found for this item."}
        self.shared_links[item_path]["enabled"] = False
        return {"success": True, "message": f"Link for '{item_path}' disabled."}