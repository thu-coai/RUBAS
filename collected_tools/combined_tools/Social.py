from BaseEnv import BaseEnv

class Social(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.tweets = []
        self.instagram_posts = []
        self.weibo_posts = []
        self.tiktok_videos = []
        self.youtube_videos = []
        self.bilibili_videos = []
        self.twitter_profiles = {}
        self.instagram_profiles = {}
        self.tiktok_profiles = {}
        self.youtube_profiles = {}
        self.bilibili_profiles = {}

    def post_tweet(self, *, content, media_urls, reply_to_id, is_sensitive=False):
        if not isinstance(content, str) or len(content) > 280:
            return {"success": False, "message": "Content must be a string up to 280 characters."}
        if not isinstance(media_urls, list) or len(media_urls) > 4:
            return {"success": False, "message": "media_urls must be a list with at most 4 items."}
        tweet_id = f"tweet_{len(self.tweets)+1}"
        tweet = {
            "id": tweet_id,
            "content": content,
            "media_urls": media_urls,
            "reply_to_id": reply_to_id,
            "is_sensitive": is_sensitive
        }
        self.tweets.append(tweet)
        return {"success": True, "data": {"tweet_id": tweet_id}}

    def post_tweet_comment(self, *, tweet_id, content, media_urls):
        if not isinstance(content, str) or len(content) > 280:
            return {"success": False, "message": "Content must be a string up to 280 characters."}
        if not isinstance(media_urls, list) or len(media_urls) > 4:
            return {"success": False, "message": "media_urls must be a list with at most 4 items."}
        comment_id = f"tweet_comment_{len(self.tweets)+1}"
        comment = {
            "id": comment_id,
            "tweet_id": tweet_id,
            "content": content,
            "media_urls": media_urls
        }
        self.tweets.append(comment)
        return {"success": True, "data": {"comment_id": comment_id}}

    def post_instagram(self, *, media_urls, caption, location, user_tags, is_sensitive=False):
        if not isinstance(media_urls, list) or len(media_urls) == 0 or len(media_urls) > 10:
            return {"success": False, "message": "media_urls must be a non-empty list with at most 10 items."}
        if not isinstance(caption, str) or len(caption) > 2200:
            return {"success": False, "message": "Caption must be a string up to 2200 characters."}
        post_id = f"insta_{len(self.instagram_posts)+1}"
        post = {
            "id": post_id,
            "media_urls": media_urls,
            "caption": caption,
            "location": location,
            "user_tags": user_tags,
            "is_sensitive": is_sensitive
        }
        self.instagram_posts.append(post)
        return {"success": True, "data": {"post_id": post_id}}

    def post_instagram_comment(self, *, post_id, content, reply_to_comment_id):
        if not isinstance(content, str) or len(content) > 2200:
            return {"success": False, "message": "Content must be a string up to 2200 characters."}
        comment_id = f"insta_comment_{len(self.instagram_posts)+1}"
        comment = {
            "id": comment_id,
            "post_id": post_id,
            "content": content,
            "reply_to_comment_id": reply_to_comment_id
        }
        self.instagram_posts.append(comment)
        return {"success": True, "data": {"comment_id": comment_id}}

    def post_weibo(self, *, content, media_urls, topics, location, is_sensitive=False, visible_to="public"):
        if not isinstance(content, str) or len(content) > 2000:
            return {"success": False, "message": "Content must be a string up to 2000 characters."}
        if not isinstance(media_urls, list) or len(media_urls) > 9:
            return {"success": False, "message": "media_urls must be a list with at most 9 items."}
        if visible_to not in ["public", "private", "friends"]:
            return {"success": False, "message": "visible_to must be one of: public, private, friends."}
        post_id = f"weibo_{len(self.weibo_posts)+1}"
        post = {
            "id": post_id,
            "content": content,
            "media_urls": media_urls,
            "topics": topics,
            "location": location,
            "is_sensitive": is_sensitive,
            "visible_to": visible_to
        }
        self.weibo_posts.append(post)
        return {"success": True, "data": {"post_id": post_id}}

    def post_weibo_comment(self, *, post_id, content, media_urls, reply_to_comment_id):
        if not isinstance(content, str) or len(content) > 1000:
            return {"success": False, "message": "Content must be a string up to 1000 characters."}
        if not isinstance(media_urls, list) or len(media_urls) > 9:
            return {"success": False, "message": "media_urls must be a list with at most 9 items."}
        comment_id = f"weibo_comment_{len(self.weibo_posts)+1}"
        comment = {
            "id": comment_id,
            "post_id": post_id,
            "content": content,
            "media_urls": media_urls,
            "reply_to_comment_id": reply_to_comment_id
        }
        self.weibo_posts.append(comment)
        return {"success": True, "data": {"comment_id": comment_id}}

    def post_tiktok(self, *, video_url, caption, sound_id, tags, allow_comments=True, allow_duet=True, allow_stitch=True):
        if not isinstance(caption, str) or len(caption) > 150:
            return {"success": False, "message": "Caption must be a string up to 150 characters."}
        video_id = f"tiktok_{len(self.tiktok_videos)+1}"
        video = {
            "id": video_id,
            "video_url": video_url,
            "caption": caption,
            "sound_id": sound_id,
            "tags": tags,
            "allow_comments": allow_comments,
            "allow_duet": allow_duet,
            "allow_stitch": allow_stitch
        }
        self.tiktok_videos.append(video)
        return {"success": True, "data": {"video_id": video_id}}

    def post_tiktok_comment(self, *, video_id, content, reply_to_comment_id):
        if not isinstance(content, str) or len(content) > 150:
            return {"success": False, "message": "Content must be a string up to 150 characters."}
        comment_id = f"tiktok_comment_{len(self.tiktok_videos)+1}"
        comment = {
            "id": comment_id,
            "video_id": video_id,
            "content": content,
            "reply_to_comment_id": reply_to_comment_id
        }
        self.tiktok_videos.append(comment)
        return {"success": True, "data": {"comment_id": comment_id}}

    def post_youtube_video(self, *, video_url, title, description, tags, category_id="22", privacy_status="public", made_for_kids=False):
        if not isinstance(title, str) or len(title) > 100:
            return {"success": False, "message": "Title must be a string up to 100 characters."}
        if not isinstance(description, str) or len(description) > 5000:
            return {"success": False, "message": "Description must be a string up to 5000 characters."}
        video_id = f"youtube_{len(self.youtube_videos)+1}"
        video = {
            "id": video_id,
            "video_url": video_url,
            "title": title,
            "description": description,
            "tags": tags,
            "category_id": category_id,
            "privacy_status": privacy_status,
            "made_for_kids": made_for_kids
        }
        self.youtube_videos.append(video)
        return {"success": True, "data": {"video_id": video_id}}

    def post_youtube_comment(self, *, video_id, content, reply_to_comment_id=None):
        if not isinstance(content, str) or len(content) > 10000:
            return {"success": False, "message": "Content must be a string up to 10000 characters."}
        comment_id = f"youtube_comment_{len(self.youtube_videos)+1}"
        comment = {
            "id": comment_id,
            "video_id": video_id,
            "content": content,
            "reply_to_comment_id": reply_to_comment_id
        }
        self.youtube_videos.append(comment)
        return {"success": True, "data": {"comment_id": comment_id}}

    def post_bilibili_video(self, *, video_url, title, partition_id, description, tags, cover_url, thread_id, copyright_type=1):
        if not isinstance(title, str) or len(title) > 80:
            return {"success": False, "message": "Title must be a string up to 80 characters."}
        if not isinstance(description, str) or len(description) > 2000:
            return {"success": False, "message": "Description must be a string up to 2000 characters."}
        video_id = f"bilibili_{len(self.bilibili_videos)+1}"
        video = {
            "id": video_id,
            "video_url": video_url,
            "title": title,
            "partition_id": partition_id,
            "description": description,
            "tags": tags,
            "cover_url": cover_url,
            "thread_id": thread_id,
            "copyright_type": copyright_type
        }
        self.bilibili_videos.append(video)
        return {"success": True, "data": {"video_id": video_id}}

    def post_bilibili_comment(self, *, video_id, content, reply_to_comment_id, include_danmaku=False, danmaku_settings=None):
        if not isinstance(content, str) or len(content) > 1000:
            return {"success": False, "message": "Content must be a string up to 1000 characters."}
        comment_id = f"bilibili_comment_{len(self.bilibili_videos)+1}"
        comment = {
            "id": comment_id,
            "video_id": video_id,
            "content": content,
            "reply_to_comment_id": reply_to_comment_id,
            "include_danmaku": include_danmaku,
            "danmaku_settings": danmaku_settings
        }
        self.bilibili_videos.append(comment)
        return {"success": True, "data": {"comment_id": comment_id}}

    def get_twitter_profile(self, *, user_id, include_pinned_tweet=False, include_metrics=True):
        profile = self.twitter_profiles.get(user_id, {
            "user_id": user_id,
            "name": f"User {user_id}",
            "bio": "This is a mock Twitter profile.",
            "pinned_tweet": "Pinned tweet content." if include_pinned_tweet else None,
            "metrics": {"followers": 123, "following": 45} if include_metrics else None
        })
        return {"success": True, "data": profile}

    def search_twitter_content(self, *, query, search_type="mixed", filters=None, limit=20, next_token=None):
        results = []
        for i in range(min(limit, 100)):
            if search_type == "users":
                results.append({"user_id": f"user_{i+1}", "username": f"user_{i+1}", "bio": "Mock user"})
            elif search_type == "tweets":
                results.append({"tweet_id": f"tweet_{i+1}", "content": f"Mock tweet about {query}"})
            else:
                results.append({"type": "mixed", "content": f"Result {i+1} for {query}"})
        return {"success": True, "data": {"results": results, "next_token": None}}

    def get_instagram_profile(self, *, user_id, include_stories=False, include_business_metrics=False):
        profile = self.instagram_profiles.get(user_id, {
            "user_id": user_id,
            "name": f"Instagram User {user_id}",
            "bio": "This is a mock Instagram profile.",
            "stories": ["Story 1", "Story 2"] if include_stories else None,
            "business_metrics": {"followers": 321, "engagement": 0.05} if include_business_metrics else None
        })
        return {"success": True, "data": profile}

    def search_instagram_content(self, *, query, search_type="top", filters=None, limit=20, next_token=None):
        results = []
        for i in range(min(limit, 100)):
            results.append({"type": search_type, "content": f"Instagram result {i+1} for {query}"})
        return {"success": True, "data": {"results": results, "next_token": None}}

    def get_tiktok_profile(self, *, user_id, include_live_status=False, include_commerce_info=False):
        profile = self.tiktok_profiles.get(user_id, {
            "user_id": user_id,
            "name": f"TikTok User {user_id}",
            "bio": "This is a mock TikTok profile.",
            "live_status": "offline" if include_live_status else None,
            "commerce_info": {"shop": "Mock Shop"} if include_commerce_info else None
        })
        return {"success": True, "data": profile}

    def search_tiktok_content(self, *, query, search_type="general", filters=None, limit=20, cursor=None):
        results = []
        for i in range(min(limit, 100)):
            results.append({"type": search_type, "content": f"TikTok result {i+1} for {query}"})
        return {"success": True, "data": {"results": results, "next_cursor": None}}

    def search_youtube_content(self, *, query, search_type="mixed", filters=None, limit=20, page_token=None):
        results = []
        for i in range(min(limit, 100)):
            results.append({"type": search_type, "content": f"YouTube result {i+1} for {query}"})
        return {"success": True, "data": {"results": results, "next_page_token": None}}

    def get_bilibili_profile(self, *, user_id, include_live=False, include_bangumi=False):
        profile = self.bilibili_profiles.get(user_id, {
            "user_id": user_id,
            "name": f"Bilibili User {user_id}",
            "bio": "This is a mock Bilibili profile.",
            "live": "offline" if include_live else None,
            "bangumi": ["Anime 1", "Anime 2"] if include_bangumi else None
        })
        return {"success": True, "data": profile}

    def search_bilibili_content(self, *, query, search_type="all", filters=None, limit=20, page=1):
        results = []
        for i in range(min(limit, 100)):
            results.append({"type": search_type, "content": f"Bilibili result {i+1} for {query}"})
        return {"success": True, "data": {"results": results, "page": page}}