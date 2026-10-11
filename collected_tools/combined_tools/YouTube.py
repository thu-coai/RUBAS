from BaseEnv import BaseEnv

class YouTube(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.users = self.parameters.get("users", [])
        self.videos = self.parameters.get("videos", [])
        self.comments = self.parameters.get("comments", [])
        self.watch_history = self.parameters.get("watch_history", {})
        self.likes = self.parameters.get("likes", {})
        self.next_video_id = 1

    def search_video(self, *, query, filters=None, limit=None):
        results = []
        for video in self.videos:
            if query.lower() in video.get("title", "").lower():
                results.append(video)
        if filters:
            # Simulate filter application (no real logic)
            pass
        if limit is not None:
            results = results[:limit]
        return {"success": True, "data": {"videos": results}}

    def update_profile(self, *, user_id, new_username=None, new_email=None, new_profile_picture=None, privacy_settings=None):
        for user in self.users:
            if user.get("id") == user_id:
                if new_username is not None:
                    user["username"] = new_username
                if new_email is not None:
                    user["email"] = new_email
                if new_profile_picture is not None:
                    user["profile_picture"] = new_profile_picture
                if privacy_settings is not None:
                    user["privacy_settings"] = privacy_settings
                return {"success": True, "message": "Profile updated."}
        return {"success": False, "message": "User not found."}

    def upload_video(self, *, video_file, title, privacy_settings, description=None, tags=None):
        video_id = f"vid{self.next_video_id}"
        self.next_video_id += 1
        video = {
            "id": video_id,
            "file": video_file,
            "title": title,
            "privacy_settings": privacy_settings,
            "description": description if description is not None else "",
            "tags": tags if tags is not None else [],
        }
        self.videos.append(video)
        return {"success": True, "data": {"video_id": video_id}}

    def view_watch_history(self, *, user_id, limit=None):
        history = self.watch_history.get(user_id, [])
        if limit is not None:
            history = history[:limit]
        return {"success": True, "data": {"watch_history": history}}

    def post_comment(self, *, video_id, user_id, comment_text):
        comment = {
            "video_id": video_id,
            "user_id": user_id,
            "text": comment_text,
        }
        self.comments.append(comment)
        return {"success": True, "message": "Comment posted."}

    def share_video(self, *, video_id, platform, share_method):
        # Simulate sharing (no real action)
        return {"success": True, "message": f"Video {video_id} shared on {platform} via {share_method}."}

    def like_dislike_video(self, *, video_id, user_id, action):
        if action not in ["like", "dislike"]:
            return {"success": False, "message": "Invalid action. Must be 'like' or 'dislike'."}
        if video_id not in self.likes:
            self.likes[video_id] = {}
        self.likes[video_id][user_id] = action
        return {"success": True, "message": f"Video {video_id} {action}d by user {user_id}."}