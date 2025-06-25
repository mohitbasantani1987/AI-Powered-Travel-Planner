import requests

class CurrencyService:
    
    EXCHANGERATE_BASE_URL = "https://api.exchangerate-api.com/v4/latest"

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate from one currency to another.
        
        Args:
            from_currency (str): Currency code to convert from.
            to_currency (str): Currency code to convert to.
        
        Returns:
            float: Exchange rate or None if an error occurs.
        """
        try:
            url = f"{self.EXCHANGERATE_BASE_URL}/{from_currency}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data['rates'].get(to_currency)
            else:
                return None
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert an amount from one currency to another.
        
        Args:
            amount (float): Amount to convert.
            from_currency (str): Currency code to convert from.
            to_currency (str): Currency code to convert to.
        
        Returns:
            float: Converted amount or None if an error occurs.
        """
        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is not None:
            return amount * rate
        return None