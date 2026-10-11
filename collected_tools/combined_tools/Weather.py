from BaseEnv import BaseEnv

class Weather(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.weather_data = self.parameters.get("weather_data", {})
        self.weather_alerts = self.parameters.get("weather_alerts", [])
        self.user_alerts = self.parameters.get("user_alerts", [])

    def get_weather(self, *, location, forecast_duration):
        # Simulate weather data lookup
        mock_weather = {
            "location": location,
            "forecast_duration": forecast_duration,
            "weather": "Sunny",
            "temperature": "25°C",
            "humidity": "50%",
            "description": f"Mock weather for {location} ({forecast_duration})"
        }
        return {"success": True, "data": mock_weather}

    def set_weather_alert(self, *, user_id, alert_condition, alert_type, alert_time):
        alert = {
            "user_id": user_id,
            "alert_condition": alert_condition,
            "alert_type": alert_type,
            "alert_time": alert_time
        }
        self.user_alerts.append(alert)
        return {"success": True, "message": "Weather alert set successfully."}

    def get_weather_alert(self, *, location, alert_type):
        # Simulate alert lookup
        mock_alert = {
            "location": location,
            "alert_type": alert_type,
            "alert": f"Mock alert: No {alert_type} expected in {location}."
        }
        return {"success": True, "data": mock_alert}