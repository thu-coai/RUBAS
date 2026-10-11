from BaseEnv import BaseEnv

class ContentModeration(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.posts = self.parameters.get("posts", [])
        self.comments = self.parameters.get("comments", [])
        self.threads = self.parameters.get("threads", [])
        self.filters = self.parameters.get("filters", {})
        self.flagged_posts = []
        self.flagged_comments = []
        self.contents = self.parameters.get("contents", [])
        self.approved_contents = []

    def fetch_statistics(self, *, stat_type, region):
        mock_stats = {
            "stat_type": stat_type,
            "region": region,
            "value": 42
        }
        return {"success": True, "data": mock_stats}

    def check_sources(self, *, content):
        credibility = "credible" if "official" in content else "unknown"
        return {"success": True, "data": {"credibility": credibility}}

    def get_content(self, *, url):
        posts = [post for post in self.posts if post.get("url") == url]
        return {"success": True, "data": {"posts": posts}}

    def flag_content(self, *, url, post_id, reason):
        for post in self.posts:
            if post.get("id") == post_id and post.get("url") == url:
                self.flagged_posts.append({"id": post_id, "url": url, "reason": reason})
                return {"success": True, "message": "Post flagged for moderation."}
        return {"success": False, "message": "Post not found."}

    def list_posts(self):
        return {"success": True, "data": {"posts": self.posts}}

    def release_post(self, *, post_id):
        for flagged in self.flagged_posts:
            if flagged["id"] == post_id:
                self.flagged_posts.remove(flagged)
                return {"success": True, "message": "Post released."}
        return {"success": False, "message": "Post not flagged."}

    def remove_post(self, *, post_id):
        for post in self.posts:
            if post.get("id") == post_id:
                self.posts.remove(post)
                return {"success": True, "message": "Post removed."}
        return {"success": False, "message": "Post not found."}

    def get_current_filters(self):
        return {"success": True, "data": {"filters": self.filters}}

    def list_threads(self):
        return {"success": True, "data": {"threads": self.threads}}

    def remove_filter_keywords(self, *, category, keyword):
        if category in self.filters and keyword in self.filters[category]:
            self.filters[category].remove(keyword)
            return {"success": True, "message": "Keyword removed from filter."}
        return {"success": False, "message": "Keyword or category not found."}

    def list_flagged_comments(self):
        return {"success": True, "data": {"flagged_comments": self.flagged_comments}}

    def delete_comment(self, *, comment_id):
        for comment in self.comments:
            if comment.get("id") == comment_id:
                self.comments.remove(comment)
                return {"success": True, "message": "Comment deleted."}
        return {"success": False, "message": "Comment not found."}

    def review_contents(self):
        return {"success": True, "data": {"contents": self.contents}}

    def approve_content(self, *, content_id):
        for content in self.contents:
            if content.get("id") == content_id:
                self.approved_contents.append(content)
                return {"success": True, "message": "Content approved."}
        return {"success": False, "message": "Content not found."}