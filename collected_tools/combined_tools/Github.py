from BaseEnv import BaseEnv

class Github(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.user = self.parameters.get("user", {"username": "owner"})
        self.repositories = self.parameters.get("repositories", [])
        self.users = self.parameters.get("users", [self.user])

    def manage_collaborator(self, *, repo_id, action, collaborator_username):
        repo = next((r for r in self.repositories if r.get("id") == repo_id), None)
        if not repo:
            return {"success": False, "message": "Repository not found."}
        if repo.get("owner") != self.user.get("username"):
            return {"success": False, "message": "User does not own the repository."}
        if "collaborators" not in repo:
            repo["collaborators"] = []
        if action == "add":
            if collaborator_username not in repo["collaborators"]:
                repo["collaborators"].append(collaborator_username)
            return {"success": True, "message": f"Collaborator {collaborator_username} added."}
        elif action == "remove":
            if collaborator_username in repo["collaborators"]:
                repo["collaborators"].remove(collaborator_username)
            return {"success": True, "message": f"Collaborator {collaborator_username} removed."}
        else:
            return {"success": False, "message": "Invalid action. Use 'add' or 'remove'."}

    def search_issues(self, *, repository_name, search_text):
        repo = next((r for r in self.repositories if r.get("name") == repository_name), None)
        if not repo:
            return {"success": False, "message": "Repository not found."}
        issues = repo.get("issues", [])
        matched = [issue for issue in issues if search_text.lower() in issue.get("title", "").lower() or search_text.lower() in issue.get("body", "").lower()]
        return {"success": True, "data": {"issues": matched}}

    def create_repository(self, *, name, visibility):
        if visibility not in ["private", "public"]:
            return {"success": False, "message": "Invalid visibility. Use 'private' or 'public'."}
        if any(r.get("name") == name for r in self.repositories):
            return {"success": False, "message": "Repository with this name already exists."}
        repo_id = f"repo{len(self.repositories)+1}"
        new_repo = {
            "id": repo_id,
            "name": name,
            "owner": self.user.get("username"),
            "visibility": visibility,
            "collaborators": [],
            "issues": [],
            "branches": ["main"]
        }
        self.repositories.append(new_repo)
        return {"success": True, "data": {"repository": new_repo}}

    def search_repositories(self, keywords=None, search_scope="all", max_results=5):
        if max_results is None or not isinstance(max_results, int) or max_results < 1:
            max_results = 5
        max_results = min(max_results, 10)
        repos = []
        if search_scope == "all":
            repos = self.repositories
        elif search_scope == "owned":
            repos = [r for r in self.repositories if r.get("owner") == self.user.get("username")]
        elif search_scope == "member":
            repos = [r for r in self.repositories if self.user.get("username") in r.get("collaborators", [])]
        else:
            return {"success": False, "message": "Invalid search_scope."}
        if keywords:
            repos = [r for r in repos if keywords.lower() in r.get("name", "").lower()]
        return {"success": True, "data": {"repositories": repos[:max_results]}}

    def get_repository_details(self, *, name):
        repo = next((r for r in self.repositories if r.get("name") == name), None)
        if not repo:
            return {"success": False, "message": "Repository not found."}
        details = {
            "id": repo.get("id"),
            "name": repo.get("name"),
            "owner": repo.get("owner"),
            "visibility": repo.get("visibility"),
            "collaborators": repo.get("collaborators", []),
            "issues": repo.get("issues", []),
            "branches": repo.get("branches", [])
        }
        return {"success": True, "data": {"repository": details}}

    def delete_repository(self, *, name):
        repo = next((r for r in self.repositories if r.get("name") == name), None)
        if not repo:
            return {"success": False, "message": "Repository not found."}
        if repo.get("owner") != self.user.get("username"):
            return {"success": False, "message": "User does not own the repository."}
        self.repositories.remove(repo)
        return {"success": True, "message": "Repository deleted."}

    def get_user_details(self, *, username):
        user = next((u for u in self.users if u.get("username") == username), None)
        if not user:
            return {"success": False, "message": "User not found."}
        user_repos = [r for r in self.repositories if r.get("owner") == username]
        member_repos = [r for r in self.repositories if username in r.get("collaborators", [])]
        details = {
            "username": user.get("username"),
            "owned_repositories": [r.get("name") for r in user_repos],
            "member_repositories": [r.get("name") for r in member_repos]
        }
        return {"success": True, "data": {"user": details}}