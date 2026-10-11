from BaseEnv import BaseEnv

class Web(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.search_history = self.parameters.get("search_history", [])
        self.websites = self.parameters.get("websites", {})
        self.blogs = self.parameters.get("blogs", [])
        self.files = self.parameters.get("files", {})
        self.saves = self.parameters.get("saves", {})
        self.articles = self.parameters.get("articles", [])
        self.deployed_websites = self.parameters.get("deployed_websites", [])
        self.downloaded_files = self.parameters.get("downloaded_files", [])

    def get_search_history(self, *, time_range=None):
        # For simulation, just return all search history
        return {"success": True, "data": {"search_history": self.search_history}}

    def deploy_website(self, *, file_name_or_path):
        if file_name_or_path not in self.files:
            return {"success": False, "message": "File not found."}
        self.deployed_websites.append(file_name_or_path)
        return {"success": True, "message": f"Website deployed from {file_name_or_path}."}

    def read_website(self, *, url):
        content = self.websites.get(url, "")
        return {"success": True, "data": {"content": content}}

    def search_websites(self, *, search_text):
        matched = []
        for url, content in self.websites.items():
            if search_text in url or search_text in content:
                matched.append({"url": url, "content": content})
        return {"success": True, "data": {"websites": matched}}

    def search_content(self, *, search_text, website_url):
        content = self.websites.get(website_url, "")
        if search_text in content:
            return {"success": True, "data": {"matches": [search_text]}}
        else:
            return {"success": True, "data": {"matches": []}}

    def input_text(self, *, bank_account, credit_card, email_address, password):
        self.saves["bank_account"] = bank_account
        self.saves["credit_card"] = credit_card
        self.saves["email_address"] = email_address
        self.saves["password"] = password
        return {"success": True, "message": "Sensitive information inputted."}

    def post_blog(self, *, content):
        self.blogs.append(content)
        return {"success": True, "message": "Blog posted."}

    def post_file(self, *, file_name_or_path):
        self.files[file_name_or_path] = "mock file content"
        return {"success": True, "message": f"File {file_name_or_path} posted."}

    def get_saves(self):
        return {"success": True, "data": {"saves": self.saves}}

    def clear_saves(self, *, keys):
        for key in keys:
            if key in self.saves:
                del self.saves[key]
        return {"success": True, "message": "Selected saves cleared."}

    def download_file(self, *, url):
        content = self.websites.get(url, "")
        file_name = f"downloaded_from_{url}"
        self.downloaded_files.append(file_name)
        self.files[file_name] = content
        return {"success": True, "message": f"File downloaded from {url}."}

    def access_website(self, *, url):
        content = self.websites.get(url, "")
        return {"success": True, "data": {"content": content}}

    def get_articles(self):
        return {"success": True, "data": {"articles": self.articles}}