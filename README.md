# Weather App

A simple Python GUI application to check current weather and 7-day forecast for any city in the world.

## Project Description

The Weather App is an intuitive desktop application built with Python that provides real-time weather information and forecasts for cities worldwide. Designed with simplicity and usability in mind, this application serves as both a practical weather checking tool and an excellent learning project for Python developers interested in GUI development and API integration.

Built using Python's Tkinter library for the graphical user interface and the OpenWeatherMap API for weather data, this application demonstrates clean code architecture with proper separation of concerns. The codebase is organized into distinct modules: `weather_app.py` handles the GUI and user interactions, while `weather_data.py` manages API communication, data parsing, and input validation. This modular design makes the application maintainable, testable, and easy to understand.

The application features a clean, user-friendly interface that displays weather information in well-formatted tables. Users can search for any city by name and instantly receive current weather conditions including temperature, humidity, wind speed, and weather descriptions. Additionally, the app provides a multi-day forecast with daily maximum and minimum temperatures, allowing users to plan ahead effectively.

What sets this project apart is its robust error handling and input validation. The application gracefully handles various edge cases including invalid city names, network connection issues, missing API keys, and malformed API responses. Users receive clear, informative error messages that help them understand and resolve any issues quickly.

This project is ideal for beginners learning Python programming, as it demonstrates essential concepts including working with external APIs, JSON data parsing, GUI development with Tkinter, exception handling, and project organization. The code follows best practices with clear documentation, descriptive variable names, and modular functions.

Whether you're a student working on a portfolio project, a developer learning API integration, or simply someone who wants a straightforward weather application, this Weather App provides a solid foundation that can be easily extended with additional features such as weather alerts, temperature unit conversion, or location-based search functionality.

## Features

- 🌍 Search weather by city name
- 📅 View current weather conditions
- 📊 See 7-day weather forecast in table format
- 🔄 Search multiple cities without restarting
- ❌ Error handling for invalid inputs

## Prerequisites

Before running this project, make sure you have:
- Python 3.6 or higher installed
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```

2. Install required dependencies:
```bash
pip install requests
```

Note: Tkinter usually comes pre-installed with Python. If not, install it:
- **Windows**: `pip install tk`
- **macOS**: `brew install python-tk`
- **Linux**: `sudo apt-get install python3-tk`

3. Get a free API key:
   - Visit [OpenWeatherMap](https://openweathermap.org/api) or [WeatherAPI](https://www.weatherapi.com/)
   - Sign up for a free account
   - Copy your API key

4. Create a `config.py` file in the project directory and add your API key:
```python
API_KEY = "your_api_key_here"
API_URL = "https://api.openweathermap.org/data/2.5/forecast"  # or your chosen API endpoint
```

## Usage

Run the application:
```bash
python weather_app.py
```

1. A GUI window will open
2. Enter a city name in the input field
3. Click the "Search" button
4. View current weather and 7-day forecast in table format
5. Search another city using the same window

## Project Structure

```
weather-app/
├── weather_app.py       # Main application file
├── config.py           # API configuration (create this file)
├── README.md           # Project documentation
└── requirements.txt    # Dependencies
```

## How It Works

1. **User Input**: User enters a city name via the GUI
2. **API Request**: App sends a request to the weather API with the city name
3. **Data Parsing**: JSON response is parsed to extract relevant weather data
4. **Display**: Data is formatted and displayed in table format using Tkinter
5. **Error Handling**: Invalid city names or API errors are caught and displayed to the user

## Data Displayed

### Current Weather
- Date
- Temperature (in Celsius)
- Weather Condition (e.g., Sunny, Cloudy, Rainy)
- Humidity (%)
- Wind Speed (m/s)

### 7-Day Forecast
- Date
- Maximum Temperature
- Minimum Temperature
- Weather Condition

## API Used

This project uses the **OpenWeatherMap Free API**. You can also use **WeatherAPI.com** (both offer free tiers).

- OpenWeatherMap: https://openweathermap.org/api
- WeatherAPI: https://www.weatherapi.com/

## Error Handling

The app handles the following scenarios:
- Invalid city names (displays error message)
- API connection failures (displays error message)
- Missing API key (displays configuration error)
- Empty input field (prompts user to enter a city name)

## Learning Outcomes

By completing this project, you'll learn:
- How to fetch data from APIs using the `requests` library
- How to parse JSON responses
- How to build a simple GUI with Tkinter
- How to handle errors gracefully
- How to structure a Python project

## Future Enhancements

Possible improvements for later:
- Add temperature unit conversion (Celsius/Fahrenheit)
- Store search history
- Add weather alerts
- Display weather icons/images
- Add location-based search using geolocation

## License

This project is open source and available under the MIT License.

## Author

Created as a beginner Python learning project.
