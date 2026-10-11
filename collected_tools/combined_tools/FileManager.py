from BaseEnv import BaseEnv

class FileManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.files = self.parameters.get("files", {})  # {filename: {"content": str, "owner": str, "shared": list, "access": dict}}
        self.folders = self.parameters.get("folders", {"/": []})  # {folder_path: [filenames/foldernames]}
        self.logged_in_user = None

    def read_file(self, *, file_name_or_path):
        if file_name_or_path not in self.files:
            return {"success": False, "message": "File not found."}
        return {"success": True, "data": {"content": self.files[file_name_or_path]["content"]}}

    def write_file(self, *, file_name_or_path, content):
        if file_name_or_path not in self.files:
            return {"success": False, "message": "File not found."}
        self.files[file_name_or_path]["content"] = content
        return {"success": True, "message": "File written successfully."}

    def share_file(self, *, file_name_or_path, access_level, to=None, owner=None):
        if file_name_or_path not in self.files:
            return {"success": False, "message": "File not found."}
        if access_level not in ["read-only", "reviewable", "editable"]:
            return {"success": False, "message": "Invalid access level."}
        if to:
            self.files[file_name_or_path].setdefault("shared", []).append(to)
            self.files[file_name_or_path].setdefault("access", {})[to] = access_level
            return {"success": True, "message": f"File shared with {to} as {access_level}."}
        else:
            public_link = f"public://{file_name_or_path}"
            self.files[file_name_or_path]["public_link"] = public_link
            self.files[file_name_or_path]["public_access_level"] = access_level
            return {"success": True, "data": {"public_link": public_link, "access_level": access_level}}

    def search_files(self, *, search_text):
        results = []
        for fname, meta in self.files.items():
            if search_text in fname or search_text in meta.get("content", ""):
                results.append(fname)
        return {"success": True, "data": {"files": results}}

    def create_file(self, *, filename, content):
        if filename in self.files:
            return {"success": False, "message": "File already exists."}
        self.files[filename] = {"content": content, "owner": self.logged_in_user, "shared": [], "access": {}}
        # Add to root folder by default
        self.folders.setdefault("/", []).append(filename)
        return {"success": True, "message": "File created successfully."}

    def delete_file(self, *, filename):
        if filename not in self.files:
            return {"success": False, "message": "File not found."}
        del self.files[filename]
        for folder, items in self.folders.items():
            if filename in items:
                items.remove(filename)
        return {"success": True, "message": "File deleted successfully."}

    def append_to_file(self, *, filename, content):
        if filename not in self.files:
            return {"success": False, "message": "File not found."}
        self.files[filename]["content"] += content
        return {"success": True, "message": "Content appended successfully."}

    def login(self, *, username):
        self.logged_in_user = username
        return {"success": True, "message": f"Logged in as {username}."}

    def list_files_and_folders(self, folder_path=None, max_results=10):
        folder = folder_path if folder_path is not None else "/"
        if folder not in self.folders:
            return {"success": False, "message": "Folder not found."}
        items = self.folders[folder][:max_results]
        return {"success": True, "data": {"items": items}}

    def list_files(self):
        return {"success": True, "data": {"files": list(self.files.keys())}}