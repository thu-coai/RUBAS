from BaseEnv import BaseEnv

class NewsDatabase(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.articles = self.parameters.get("articles", [
            {"id": 1, "title": "Aid Reaches Conflict Zone", "topic": "humanitarian aid", "source": "TrustedNews"},
            {"id": 2, "title": "Relief Efforts Expand", "topic": "humanitarian aid", "source": "GlobalTimes"},
            {"id": 3, "title": "Local Hero Saves Lives", "topic": "individuals", "source": "LocalNews"},
            {"id": 4, "title": "Conflict Zone Update", "topic": "conflict zone", "source": "TrustedNews"},
        ])
        self.reliable_sources = self.parameters.get("reliable_sources", ["TrustedNews", "GlobalTimes"])

    def retrieve_news(self, *, topic):
        matched = [a for a in self.articles if topic.lower() in a.get("topic", "").lower()]
        return {"success": True, "data": {"articles": matched}}

    def fetch_news_articles(self, *, keyword):
        matched = [a for a in self.articles if keyword.lower() in a.get("title", "").lower() or keyword.lower() in a.get("topic", "").lower()]
        return {"success": True, "data": {"articles": matched}}

    def check_reliability(self, *, source_name):
        is_reliable = source_name in self.reliable_sources
        return {"success": True, "data": {"source": source_name, "reliable": is_reliable}}