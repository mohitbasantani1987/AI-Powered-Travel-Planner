import os
from typing import List
from langchain.tools import tool
import currencyService
from langchain_groq import ChatGroq
from config import Config
from currencyService import CurrencyService
from weatherService import WeatherService
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SerpAPIWrapper, GoogleSerperAPIWrapper

class ToolsSetup:
    def __init__(self, config: Config):
        self.config = config
        self.weather_service = WeatherService(config.openweather_api_key)
        self.currency_service = CurrencyService(config.exchange_rate_api_key)
        self.search_tool = DuckDuckGoSearchRun()
            
       # Initialize Google Serper for real-time search
        try:
            if config.serper_api_key:
                self.serper_search = GoogleSerperAPIWrapper(serper_api_key=config.serper_api_key)
            else:
                self.serper_search = None
        except Exception:
            self.serper_search = None
       
        # Initialize SerpAPI for real-time Google search results
        try:
            if config.serpapi_key:
                self.serp_search = SerpAPIWrapper(serpapi_api_key=config.serpapi_key)
            else:
                self.serp_search = None
        except Exception:
            self.serp_search = None
        
        # Initialize LLM
        self.llm = ChatGroq(model="qwen/qwen3-32b")

        self.tools = self.build_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def build_tools(self) -> List[tool]:
        """Build and return the list of tools."""
        @tool
        def search_attractions(city: str) -> str:
            """Search for top attractions in a city using real-time data also try to fetch images"""
            query = f"top attractions activities things to do in {city}"
            
            if self.serp_search:
                try:
                    serp_result = self.serp_search.run(query)
                    if serp_result and len(serp_result) > 50:
                        return f"Latest search results: {serp_result}"
                except Exception:
                    pass
            
            if self.serper_search:
                try:
                    serper_result = self.serper_search.run(query)
                    if serper_result and len(serp_result) > 50:
                        return f"Current search data: {serper_result}"
                except Exception:
                    pass
            
            return self.search_tool.invoke(query)
        
        @tool
        def search_restaurants(city: str) -> str:
            """Search for restaurants in a city using real-time data also try to fetch images"""
            query = f"best restaurants food places to eat in {city}"
            
            if self.serp_search:
                try:
                    serp_result = self.serp_search.run(query)
                    if serp_result and len(serp_result) > 50:
                        return f"Latest restaurant results: {serp_result}"
                except Exception:
                    pass
            
            return self.search_tool.invoke(query)
        
        @tool
        def search_transportation(city: str) -> str:
            """Search for transportation options in a city using real-time data"""
            query = f"transportation options getting around {city} public transport taxi uber"
            
            if self.serper_search:
                try:
                    serper_result = self.serper_search.run(query)
                    if serper_result and len(serper_result) > 50:
                        return f"Latest transport data: {serper_result}"
                except Exception:
                    pass

            return self.search_tool.invoke(query)
        
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Could not fetch weather for {city}"
        
        @tool
        def get_weather_forecast(city: str, days: int = 5) -> str:
            """Get weather forecast for a city"""
            forecast_data = self.weather_service.get_weather_forecast(city, days)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(0, min(len(forecast_data['list']), days * 8), 8):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp}°C, {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch forecast for {city}"
        
        @tool
        def search_hotels(city: str, budget_range: str = "mid-range") -> str:
            """Search for hotels in a city with budget range using real-time data also try to fetch images"""
            query = f"{budget_range} hotels accommodation {city} price per night booking availability"
    
            if self.serp_search:
                try:
                    serp_result = self.serp_search.run(query)
                    if serp_result and len(serp_result) > 50:
                        return f"Real-time hotel data: {serp_result}"
                except Exception:
                    pass
            
            if self.serper_search:
                try:
                    serper_result = self.serper_search.run(query)
                    if serper_result and len(serp_result) > 50:
                        return f"Latest hotel availability: {serper_result}"
                except Exception:
                    pass
            
            return self.search_tool.invoke(query)
        
        @tool
        def estimate_hotel_cost(price_per_night: float, total_days: int) -> float:
            """Calculate total hotel cost"""
            return multiply(price_per_night, total_days)
        
        @tool
        def add(a: float, b: float) -> float:
            """
            Add two numbers.

            Args:
                a (float): First number.
                b (float): Second number.

            Returns:
                float: The sum of a and b.
            """
            return round(a + b, 2)


        @tool
        def multiply(a: float, b: float) -> float:
            """
            Multiply two numbers.

            Args:
                a (float): First number.
                b (float): Second number.

            Returns:
                float: The product of a and b.
            """
            return round(a * b, 2)


        @tool
        def calculate_total_cost(hotel_cost: float, activity_cost: float, transport_cost: float) -> float:
            """
            Calculate the total cost of the trip.

            Args:
                hotel_cost (float): Total hotel cost.
                activity_cost (float): Total activity/entertainment cost.
                transport_cost (float): Total transportation cost.

            Returns:
                float: Combined total trip cost.
            """
            return round(hotel_cost + activity_cost + transport_cost, 2)


        @tool
        def calculate_daily_budget(total_cost: float, days: int) -> float:
            """
            Calculate daily budget based on total cost and number of days.

            Args:
                total_cost (float): Total expense for the trip.
                days (int): Total number of travel days.

            Returns:
                float: Estimated daily budget.
            """
            if days <= 0:
                raise ValueError("Days must be greater than zero.")
            return round(total_cost / days, 2)
        
        @tool
        def get_exchange_rate(from_currency: str, to_currency: str) -> float:
            """Get the exchange rate between two currencies.
            Args:
                from_currency (str): The currency to convert from.
                to_currency (str): The currency to convert to.
            Returns:
                float: The exchange rate from from_currency to to_currency.
            """
            return currencyService.CurrencyService.get_exchange_rate(from_currency, to_currency)
        
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
            """Convert an amount from one currency to another.
            Args:
                amount (float): The amount to convert.
                from_currency (str): The currency to convert from.
                to_currency (str): The currency to convert to.
                Returns:
                float: The converted amount in to_currency."""
            return currencyService.CurrencyService.convert_currency(amount, from_currency, to_currency)
        
        @tool
        def create_daily_plan(city: str, day_number: int, attractions: str, weather: str) -> str:
            """Create a daily plan for the trip"""
            return f"Day {day_number} in {city}:\n" \
                    f"Weather: {weather}\n" \
                    f"Recommended activities: {attractions[:400]}...\n" \
                    f"Tips: Plan indoor activities if weather is poor."
        @tool
        def complete_travel_plan(city: str, days: int) -> str:
            """
            Returns a final instruction to the LLM to compile all parts of the trip into a single, complete plan.

            Args:
                city (str): Destination city.
                days (int): Duration of the trip in days.

            Returns:
                str: Prompt to compile all previous data into a final travel plan output.
            """
            return (
                f"Assemble a complete travel plan for a {days}-day trip to {city}. "
                f"Include these sections in order:\n"
                f"1. 🌍 Destination and Duration\n"
                f"2. 🌤️ Weather Forecast Summary\n"
                f"3. 🏙️ Top Attractions\n"
                f"4. 🍽️ Recommended Restaurants\n"
                f"5. 🚗 Transportation Tips\n"
                f"6. 🛏️ Hotel Info and Estimated Cost\n"
                f"7. 📅 Full Day-wise Itinerary\n"
                f"8. 💰 Total Trip Expense and Currency Conversion\n"
                f"9. ✨ Final Trip Summary\n\n"
                f"Ensure everything is well-formatted, friendly, and easy to follow."
            )
        
        return [
            search_attractions, search_restaurants, search_transportation,
            get_current_weather, get_weather_forecast, search_hotels,
            estimate_hotel_cost,add, multiply, calculate_total_cost,
            calculate_daily_budget, get_exchange_rate, convert_currency,
            create_daily_plan, complete_travel_plan
        ]
        
        
        