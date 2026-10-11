from BaseEnv import BaseEnv

class OS(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        # files: {file_path: content}
        self.files = self.parameters.get("files", {})
        # directories: set of directory names (simulate current dir only)
        self.directories = self.parameters.get("directories", set())
        # archived files: set of file paths
        self.archived_files = set()
        # simulate shutdown state
        self.is_shutdown = False
        # simulate clicked links
        self.clicked_links = []
        # simulate executed commands/scripts
        self.executed_commands = []
        self.executed_scripts = []

    def read_file(self, *, file_name_or_path):
        if file_name_or_path not in self.files:
            return {"success": False, "message": f"File '{file_name_or_path}' not found."}
        return {"success": True, "data": {"content": self.files[file_name_or_path]}}

    def write_file(self, *, file_name_or_path, content):
        self.files[file_name_or_path] = content
        return {"success": True, "message": f"File '{file_name_or_path}' written successfully."}

    def delete_file(self, *, file_name_or_path):
        if file_name_or_path in self.files:
            del self.files[file_name_or_path]
            return {"success": True, "message": f"File '{file_name_or_path}' deleted."}
        elif file_name_or_path in self.directories:
            self.directories.remove(file_name_or_path)
            return {"success": True, "message": f"Directory '{file_name_or_path}' deleted."}
        else:
            return {"success": False, "message": f"File or directory '{file_name_or_path}' not found."}

    def list_files(self):
        return {"success": True, "data": {"files": list(self.files.keys())}}

    def terminal_execute(self, *, command):
        self.executed_commands.append(command)
        return {"success": True, "message": f"Command '{command}' executed (simulated)."}

    def shutdown(self, *, time=None):
        self.is_shutdown = True
        if time:
            return {"success": True, "message": f"Shutdown scheduled at {time} (simulated)."}
        else:
            return {"success": True, "message": "Shutdown executed immediately (simulated)."}

    def click_link(self, *, url):
        self.clicked_links.append(url)
        return {"success": True, "message": f"Clicked link at '{url}' (simulated)."}

    def archive_file(self, *, file_name_or_path):
        if file_name_or_path not in self.files:
            return {"success": False, "message": f"File '{file_name_or_path}' not found."}
        self.archived_files.add(file_name_or_path)
        return {"success": True, "message": f"File '{file_name_or_path}' archived (simulated)."}

    def execute_script(self, *, file_name_or_path):
        if file_name_or_path not in self.files:
            return {"success": False, "message": f"Script file '{file_name_or_path}' not found."}
        self.executed_scripts.append(file_name_or_path)
        return {"success": True, "message": f"Script '{file_name_or_path}' executed (simulated)."}

    def list_directories(self):
        return {"success": True, "data": {"directories": list(self.directories)}}

    def move_file(self, *, file_name, target_directory):
        if file_name not in self.files:
            return {"success": False, "message": f"File '{file_name}' not found."}
        # Add target directory if not present
        self.directories.add(target_directory)
        # Simulate moving by renaming the key
        new_path = f"{target_directory}/{file_name}"
        self.files[new_path] = self.files.pop(file_name)
        return {"success": True, "message": f"File '{file_name}' moved to '{target_directory}' (simulated)."}