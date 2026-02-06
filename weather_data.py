"""
Weather data module - handles API communication, data parsing, and input validation.
Separated from GUI to allow independent testing.
"""

from datetime import datetime
from collections import defaultdict
import requests

# Import API configuration
try:
    from config import API_KEY, CURRENT_WEATHER_URL, FORECAST_URL
except ImportError:
    API_KEY = None
    CURRENT_WEATHER_URL = None
    FORECAST_URL = None


def validate_input(city_name):
    """Validate user input for city name.

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not city_name or city_name.strip() == "":
        return False, "Please enter a city name."
    if not all(c.isalpha() or c.isspace() or c in "-'.," for c in city_name.strip()):
        return False, "City name contains invalid characters."
    return True, ""


def fetch_current_weather(city_name):
    """Fetch current weather data from OpenWeatherMap API.

    Raises:
        ValueError: For invalid city or missing API key.
        ConnectionError: For API errors.
    """
    if not API_KEY:
        raise ValueError("API key is missing. Please set it in config.py.")

    params = {
        "q": city_name.strip(),
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise ValueError(f"City '{city_name}' not found. Please check the name.")
    elif response.status_code == 401:
        raise ValueError("Invalid API key. Please check config.py.")
    elif response.status_code != 200:
        raise ConnectionError(f"API error (status {response.status_code}).")

    return response.json()


def fetch_forecast(city_name):
    """Fetch forecast data from OpenWeatherMap API.

    Raises:
        ValueError: For invalid city or missing API key.
        ConnectionError: For API errors.
    """
    if not API_KEY:
        raise ValueError("API key is missing. Please set it in config.py.")

    params = {
        "q": city_name.strip(),
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise ValueError(f"City '{city_name}' not found. Please check the name.")
    elif response.status_code == 401:
        raise ValueError("Invalid API key. Please check config.py.")
    elif response.status_code != 200:
        raise ConnectionError(f"API error (status {response.status_code}).")

    return response.json()


def parse_current_weather(data):
    """Parse current weather JSON response into a dictionary."""
    return {
        "temperature": f"{data['main']['temp']:.1f} °C",
        "condition": data["weather"][0]["description"].title(),
        "humidity": f"{data['main']['humidity']}%",
        "wind_speed": f"{data['wind']['speed']} m/s"
    }


def parse_forecast(data):
    """Parse forecast JSON response into a list of daily forecasts.

    The free-tier API returns 3-hour interval forecasts for 5 days.
    This function groups them by date and extracts daily max/min temps.
    """
    daily = defaultdict(lambda: {"temps": [], "conditions": []})

    for item in data["list"]:
        date_str = item["dt_txt"].split(" ")[0]
        daily[date_str]["temps"].append(item["main"]["temp"])
        daily[date_str]["conditions"].append(item["weather"][0]["description"])

    forecast_list = []
    for date_str in sorted(daily.keys()):
        info = daily[date_str]
        # Pick the most common weather condition for the day
        condition = max(set(info["conditions"]), key=info["conditions"].count)
        forecast_list.append({
            "date": datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %b %d"),
            "max_temp": f"{max(info['temps']):.1f} °C",
            "min_temp": f"{min(info['temps']):.1f} °C",
            "condition": condition.title()
        })

    return forecast_list
