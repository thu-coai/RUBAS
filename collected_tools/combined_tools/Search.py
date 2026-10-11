from BaseEnv import BaseEnv

class Search(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.search_history = self.parameters.get("search_history", [])
        self.mock_trends = [
            {"query": "weather", "popularity": 95},
            {"query": "news", "popularity": 90},
            {"query": "sports", "popularity": 85},
        ]

    def search_google(
        self,
        *,
        query,
        num_results=10,
        search_type="web",
        language="en",
        safe_search=True,
        time_period=None,
        region="US"
    ):
        if not isinstance(query, str) or not query:
            return {"success": False, "message": "Invalid or missing query."}
        if not isinstance(num_results, int) or not (1 <= num_results <= 50):
            return {"success": False, "message": "num_results must be between 1 and 50."}
        if search_type not in ["web", "images", "news", "videos"]:
            return {"success": False, "message": "Invalid search_type."}
        self.search_history.append(
            {
                "engine": "google",
                "query": query,
                "type": search_type,
                "language": language,
                "region": region,
            }
        )
        results = [
            {
                "title": f"Google {search_type.capitalize()} Result {i+1}",
                "url": f"https://google.com/search?q={query}&result={i+1}",
            }
            for i in range(num_results)
        ]
        return {"success": True, "data": {"results": results}}

    def search_bing(
        self,
        *,
        query,
        count=10,
        search_type="web",
        market="en-US",
        safe_search="moderate",
        freshness=None,
        response_filter=None
    ):
        if not isinstance(query, str) or not query:
            return {"success": False, "message": "Invalid or missing query."}
        if not isinstance(count, int) or not (1 <= count <= 50):
            return {"success": False, "message": "count must be between 1 and 50."}
        if search_type not in ["web", "images", "news", "videos"]:
            return {"success": False, "message": "Invalid search_type."}
        if safe_search not in ["off", "moderate", "strict"]:
            return {"success": False, "message": "Invalid safe_search value."}
        self.search_history.append(
            {
                "engine": "bing",
                "query": query,
                "type": search_type,
                "market": market,
            }
        )
        results = [
            {
                "title": f"Bing {search_type.capitalize()} Result {i+1}",
                "url": f"https://bing.com/search?q={query}&result={i+1}",
            }
            for i in range(count)
        ]
        return {"success": True, "data": {"results": results}}

    def search_brave(
        self,
        *,
        query,
        count=10,
        search_type="web",
        country="us",
        search_filter=None,
        ui_language="en-US",
        no_tracking=True
    ):
        if not isinstance(query, str) or not query:
            return {"success": False, "message": "Invalid or missing query."}
        if not isinstance(count, int) or not (1 <= count <= 50):
            return {"success": False, "message": "count must be between 1 and 50."}
        if search_type not in ["web", "images", "news", "videos"]:
            return {"success": False, "message": "Invalid search_type."}
        if search_filter is not None and search_filter not in ["moderate", "strict"]:
            return {"success": False, "message": "Invalid search_filter."}
        self.search_history.append(
            {
                "engine": "brave",
                "query": query,
                "type": search_type,
                "country": country,
            }
        )
        results = [
            {
                "title": f"Brave {search_type.capitalize()} Result {i+1}",
                "url": f"https://search.brave.com/search?q={query}&result={i+1}",
            }
            for i in range(count)
        ]
        return {"success": True, "data": {"results": results}}

    def search_baidu(
        self,
        *,
        query,
        rn=10,
        search_type="web",
        region="cn",
        time_range=None,
        safe=True,
        lang_type="zh"
    ):
        if not isinstance(query, str) or not query:
            return {"success": False, "message": "Invalid or missing query."}
        if not isinstance(rn, int) or not (1 <= rn <= 50):
            return {"success": False, "message": "rn must be between 1 and 50."}
        if search_type not in ["web", "images", "news", "videos"]:
            return {"success": False, "message": "Invalid search_type."}
        if lang_type not in ["zh", "en"]:
            return {"success": False, "message": "Invalid lang_type."}
        self.search_history.append(
            {
                "engine": "baidu",
                "query": query,
                "type": search_type,
                "region": region,
            }
        )
        results = [
            {
                "title": f"Baidu {search_type.capitalize()} Result {i+1}",
                "url": f"https://baidu.com/s?wd={query}&result={i+1}",
            }
            for i in range(rn)
        ]
        return {"success": True, "data": {"results": results}}

    def image_search(self, *, keyword, num_results=10, filters=None):
        if not isinstance(keyword, str) or not keyword:
            return {"success": False, "message": "Invalid or missing keyword."}
        if not isinstance(num_results, int) or num_results < 1:
            return {"success": False, "message": "num_results must be >= 1."}
        self.search_history.append(
            {
                "engine": "google",
                "query": keyword,
                "type": "images",
                "filters": filters,
            }
        )
        results = [
            {
                "title": f"Image Result {i+1}",
                "url": f"https://images.google.com/search?q={keyword}&img={i+1}",
            }
            for i in range(num_results)
        ]
        return {"success": True, "data": {"results": results}}

    def video_search(self, *, keyword, num_results=10, filters=None):
        if not isinstance(keyword, str) or not keyword:
            return {"success": False, "message": "Invalid or missing keyword."}
        if not isinstance(num_results, int) or num_results < 1:
            return {"success": False, "message": "num_results must be >= 1."}
        self.search_history.append(
            {
                "engine": "google",
                "query": keyword,
                "type": "videos",
                "filters": filters,
            }
        )
        results = [
            {
                "title": f"Video Result {i+1}",
                "url": f"https://video.google.com/search?q={keyword}&vid={i+1}",
            }
            for i in range(num_results)
        ]
        return {"success": True, "data": {"results": results}}

    def news_search(self, *, keyword, num_results=10, filters=None):
        if not isinstance(keyword, str) or not keyword:
            return {"success": False, "message": "Invalid or missing keyword."}
        if not isinstance(num_results, int) or num_results < 1:
            return {"success": False, "message": "num_results must be >= 1."}
        self.search_history.append(
            {
                "engine": "google",
                "query": keyword,
                "type": "news",
                "filters": filters,
            }
        )
        results = [
            {
                "title": f"News Result {i+1}",
                "url": f"https://news.google.com/search?q={keyword}&news={i+1}",
            }
            for i in range(num_results)
        ]
        return {"success": True, "data": {"results": results}}

    def get_search_trends(self, time_range="past 7 days", location="global"):
        # Simulate returning mock trends
        return {
            "success": True,
            "data": {
                "trends": self.mock_trends,
                "time_range": time_range,
                "location": location,
            },
        }

    def get_search_history(self, time_range=None):
        # Simulate filtering by time_range (not implemented, just return all)
        return {"success": True, "data": {"history": self.search_history}}