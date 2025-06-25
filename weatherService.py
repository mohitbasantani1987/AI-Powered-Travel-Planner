import requests

class WeatherService:

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, city)-> dict:
        """Get current weather for a city.
        Args:
            city (str): Name of the city.
        Returns:
            dict: Current weather data or None if an error occurs.
        """
        try:
            url = f"{self.BASE_URL}/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception:
            return None
        
    def get_weather_forecast(self, city, days=5)-> dict:
        """Get weather forecast for a city.
        Args:
            city (str): Name of the city.
            days (int): Number of days for the forecast (default is 5).
        Returns:
            dict: Weather forecast data or None if an error occurs.
        """
        try:
            url = f"{self.BASE_URL}/forecast?q={city}&appid={self.api_key}&units=metric&cnt={days * 8}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception:
            return None    