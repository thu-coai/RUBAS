from BaseEnv import BaseEnv

class InfoProcess(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.dictionary = self.parameters.get("dictionary", {
            "python": "A high-level programming language.",
            "weather": "The state of the atmosphere at a place and time.",
            "history": "The study of past events."
        })
        self.history = self.parameters.get("history", {
            "01-01": ["New Year's Day"],
            "07-04": ["Independence Day (USA)"],
            "12-25": ["Christmas Day"]
        })
        self.articles = self.parameters.get("articles", [
            {"title": "Python Basics", "keyword": "python"},
            {"title": "Weather Patterns", "keyword": "weather"},
            {"title": "World History", "keyword": "history"}
        ])
        self.videos = self.parameters.get("videos", [
            "The Matrix",
            "Inception",
            "Finding Nemo"
        ])

    def image_description(self, *, url):
        if not isinstance(url, str) or not url.lower().endswith(('.jpg', '.jpeg', '.png')):
            return {"success": False, "message": "Invalid image URL. Must end with .jpg, .jpeg, or .png."}
        return {"success": True, "data": {"description": f"Simulated description for image at {url}."}}

    def dictionary(self, *, keyword):
        if not isinstance(keyword, str):
            return {"success": False, "message": "Keyword must be a string."}
        definition = self.dictionary.get(keyword.lower(), "No definition found.")
        return {"success": True, "data": {"definition": definition}}

    def query_history_today(self, *, date):
        if not isinstance(date, str):
            return {"success": False, "message": "Date must be a string in format MM-DD."}
        events = self.history.get(date, [])
        return {"success": True, "data": {"events": events}}

    def search_keyword(self, *, keyword):
        if not isinstance(keyword, str):
            return {"success": False, "message": "Keyword must be a string."}
        return {"success": True, "data": {"results": [f"Simulated search result for '{keyword}'."]}}

    def search_articles(self, *, keyword):
        if not isinstance(keyword, str):
            return {"success": False, "message": "Keyword must be a string."}
        found = [article for article in self.articles if keyword.lower() in article.get("keyword", "").lower()]
        return {"success": True, "data": {"articles": found}}

    def document_description(self, *, url):
        if not isinstance(url, str) or not url.lower().endswith('.txt'):
            return {"success": False, "message": "Invalid document URL. Must end with .txt."}
        return {"success": True, "data": {"description": f"Simulated description for document at {url}."}}

    def speech_recognition(self, *, url):
        if not isinstance(url, str) or not url.lower().endswith('.wav'):
            return {"success": False, "message": "Invalid audio URL. Must end with .wav."}
        return {"success": True, "data": {"transcript": f"Simulated transcript for audio at {url}."}}

    def get_weather_for_coordinates(self, *, latitude, longitude):
        if not isinstance(latitude, str) or not isinstance(longitude, str):
            return {"success": False, "message": "Latitude and longitude must be strings."}
        return {"success": True, "data": {"weather": f"Simulated weather at ({latitude}, {longitude})."}}

    def clothing_recommendation(self, *, temperature, weather_conditions):
        if not isinstance(temperature, str) or not isinstance(weather_conditions, str):
            return {"success": False, "message": "Temperature and weather_conditions must be strings."}
        try:
            temp = float(temperature)
        except ValueError:
            return {"success": False, "message": "Temperature must be a number in string format."}
        if temp < 10:
            rec = "Wear a coat."
        elif temp < 20:
            rec = "Wear a jacket."
        else:
            rec = "Wear light clothing."
        rec += f" Weather: {weather_conditions}."
        return {"success": True, "data": {"recommendation": rec}}

    def video_recommendation(self):
        return {"success": True, "data": {"videos": self.videos}}