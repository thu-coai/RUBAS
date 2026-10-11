from BaseEnv import BaseEnv

class EvernoteManager(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.notes = self.parameters.get("notes", [])
        self.notebooks = self.parameters.get("notebooks", [])
        self.note_id_counter = 1
        self.notebook_id_counter = 1
        # Each note: {"id": str, "title": str, "content": str, "attachments": list, "notebook_id": str, "tags": list, "sharing": dict}
        # Each notebook: {"id": str, "name": str}

    def create_note(self, *, title, content, attachments=None, notebook_id=None):
        note_id = f"note_{self.note_id_counter}"
        self.note_id_counter += 1
        note = {
            "id": note_id,
            "title": title,
            "content": content,
            "attachments": attachments if attachments is not None else [],
            "notebook_id": notebook_id,
            "tags": [],
            "sharing": {}
        }
        self.notes.append(note)
        return {"success": True, "data": {"note_id": note_id}}

    def read_note(self, *, note_id):
        for note in self.notes:
            if note["id"] == note_id:
                return {"success": True, "data": {"note": note}}
        return {"success": False, "message": "Note not found."}

    def update_note(self, *, note_id, title=None, content=None, attachments=None):
        for note in self.notes:
            if note["id"] == note_id:
                if title is not None:
                    note["title"] = title
                if content is not None:
                    note["content"] = content
                if attachments is not None:
                    note["attachments"] = attachments
                return {"success": True, "data": {"note": note}}
        return {"success": False, "message": "Note not found."}

    def delete_note(self, *, note_id):
        for note in self.notes:
            if note["id"] == note_id:
                self.notes.remove(note)
                return {"success": True, "message": "Note deleted."}
        return {"success": False, "message": "Note not found."}

    def create_notebook(self, *, name):
        notebook_id = f"notebook_{self.notebook_id_counter}"
        self.notebook_id_counter += 1
        notebook = {
            "id": notebook_id,
            "name": name
        }
        self.notebooks.append(notebook)
        return {"success": True, "data": {"notebook_id": notebook_id}}

    def read_notebook(self, *, notebook_id):
        for notebook in self.notebooks:
            if notebook["id"] == notebook_id:
                notes_in_notebook = [note for note in self.notes if note.get("notebook_id") == notebook_id]
                return {"success": True, "data": {"notebook": notebook, "notes": notes_in_notebook}}
        return {"success": False, "message": "Notebook not found."}

    def update_notebook(self, *, notebook_id, name):
        for notebook in self.notebooks:
            if notebook["id"] == notebook_id:
                notebook["name"] = name
                return {"success": True, "data": {"notebook": notebook}}
        return {"success": False, "message": "Notebook not found."}

    def delete_notebook(self, *, notebook_id):
        for notebook in self.notebooks:
            if notebook["id"] == notebook_id:
                self.notebooks.remove(notebook)
                # Optionally, remove notebook_id from notes
                for note in self.notes:
                    if note.get("notebook_id") == notebook_id:
                        note["notebook_id"] = None
                return {"success": True, "message": "Notebook deleted."}
        return {"success": False, "message": "Notebook not found."}

    def search_notes(self, *, keywords=None, tags=None, notebook_id=None, max_results=10):
        results = self.notes
        if notebook_id is not None:
            results = [note for note in results if note.get("notebook_id") == notebook_id]
        if keywords is not None and len(keywords) > 0:
            results = [
                note for note in results
                if any(
                    kw.lower() in note.get("title", "").lower() or
                    kw.lower() in note.get("content", "").lower()
                    for kw in keywords
                )
            ]
        if tags is not None and len(tags) > 0:
            results = [
                note for note in results
                if any(tag in note.get("tags", []) for tag in tags)
            ]
        results = results[:max_results]
        return {"success": True, "data": {"notes": results}}

    def manage_note_sharing_level(self, *, note_id, email, level):
        if level not in ["not_accessible", "read_only", "can_edit"]:
            return {"success": False, "message": "Invalid sharing level."}
        for note in self.notes:
            if note["id"] == note_id:
                note["sharing"][email] = level
                return {"success": True, "message": f"Sharing level set to {level} for {email}."}
        return {"success": False, "message": "Note not found."}

    def search_notebooks(self, *, keywords=None, name=None, max_results=10):
        results = self.notebooks
        if name is not None:
            results = [nb for nb in results if nb.get("name", "").lower() == name.lower()]
        if keywords is not None and len(keywords) > 0:
            results = [
                nb for nb in results
                if any(kw.lower() in nb.get("name", "").lower() for kw in keywords)
            ]
        results = results[:max_results]
        return {"success": True, "data": {"notebooks": results}}