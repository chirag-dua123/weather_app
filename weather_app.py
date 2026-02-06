"""
Weather Application using Tkinter GUI
Fetches current weather and 5-day forecast from OpenWeatherMap API
"""

import tkinter as tk
import requests

from weather_data import (
    validate_input,
    fetch_current_weather,
    fetch_forecast,
    parse_current_weather,
    parse_forecast,
    API_KEY,
)


def clear_frame(frame):
    """Remove all widgets from a frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def create_current_weather_table(parent, weather_data):
    """Create a table displaying current weather information."""
    clear_frame(parent)

    headers = ["Parameter", "Value"]
    rows = [
        ("Temperature", weather_data["temperature"]),
        ("Condition", weather_data["condition"]),
        ("Humidity", weather_data["humidity"]),
        ("Wind Speed", weather_data["wind_speed"]),
    ]

    # Header row
    for col, header in enumerate(headers):
        lbl = tk.Label(parent, text=header, font=("Arial", 11, "bold"),
                       borderwidth=1, relief="solid", padx=10, pady=5,
                       bg="#4a90d9", fg="white")
        lbl.grid(row=0, column=col, sticky="nsew")

    # Data rows
    for row_idx, (param, value) in enumerate(rows, start=1):
        bg = "#f0f4f8" if row_idx % 2 == 0 else "white"
        tk.Label(parent, text=param, font=("Arial", 10),
                 borderwidth=1, relief="solid", padx=10, pady=4,
                 bg=bg).grid(row=row_idx, column=0, sticky="nsew")
        tk.Label(parent, text=value, font=("Arial", 10),
                 borderwidth=1, relief="solid", padx=10, pady=4,
                 bg=bg).grid(row=row_idx, column=1, sticky="nsew")

    # Make columns expand evenly
    parent.columnconfigure(0, weight=1)
    parent.columnconfigure(1, weight=1)


def create_forecast_table(parent, forecast_data):
    """Create a table displaying the forecast information."""
    clear_frame(parent)

    headers = ["Date", "Max Temp", "Min Temp", "Condition"]

    # Header row
    for col, header in enumerate(headers):
        lbl = tk.Label(parent, text=header, font=("Arial", 11, "bold"),
                       borderwidth=1, relief="solid", padx=10, pady=5,
                       bg="#4a90d9", fg="white")
        lbl.grid(row=0, column=col, sticky="nsew")

    # Data rows
    for row_idx, day in enumerate(forecast_data, start=1):
        bg = "#f0f4f8" if row_idx % 2 == 0 else "white"
        values = [day["date"], day["max_temp"], day["min_temp"], day["condition"]]
        for col, value in enumerate(values):
            tk.Label(parent, text=value, font=("Arial", 10),
                     borderwidth=1, relief="solid", padx=10, pady=4,
                     bg=bg).grid(row=row_idx, column=col, sticky="nsew")

    # Make columns expand evenly
    for col in range(4):
        parent.columnconfigure(col, weight=1)


class WeatherApp:
    """Main Weather Application class."""

    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)

        self._build_ui()

    def _build_ui(self):
        """Build the main application UI."""
        # Title label
        title_lbl = tk.Label(self.root, text="Weather Forecast",
                             font=("Arial", 18, "bold"), pady=10)
        title_lbl.pack()

        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="City:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.city_entry = tk.Entry(search_frame, font=("Arial", 12), width=25)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.bind("<Return>", lambda e: self.search_weather())

        search_btn = tk.Button(search_frame, text="Search", font=("Arial", 12),
                               command=self.search_weather, bg="#4a90d9", fg="white")
        search_btn.pack(side=tk.LEFT, padx=5)

        # Status label for errors / info
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10),
                                     fg="red")
        self.status_label.pack(pady=2)

        # Current weather section
        tk.Label(self.root, text="Current Weather",
                 font=("Arial", 14, "bold")).pack(pady=(10, 2))

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.X, padx=20, pady=5)

        # Forecast section
        tk.Label(self.root, text="Forecast (up to 5 days, 3-hour intervals grouped by day)",
                 font=("Arial", 14, "bold")).pack(pady=(10, 2))

        self.forecast_frame = tk.Frame(self.root)
        self.forecast_frame.pack(fill=tk.X, padx=20, pady=5)

    def search_weather(self):
        """Handle the search button click."""
        city = self.city_entry.get()
        self.status_label.config(text="")

        # Validate input
        valid, msg = validate_input(city)
        if not valid:
            self.status_label.config(text=msg)
            return

        # Check API key
        if not API_KEY:
            self.status_label.config(text="API key is missing. Please configure config.py.")
            return

        try:
            self.status_label.config(text="Fetching weather data...", fg="blue")
            self.root.update_idletasks()

            # Fetch and display current weather
            current_data = fetch_current_weather(city)
            parsed_current = parse_current_weather(current_data)
            create_current_weather_table(self.current_frame, parsed_current)

            # Fetch and display forecast
            forecast_data = fetch_forecast(city)
            parsed_forecast = parse_forecast(forecast_data)
            create_forecast_table(self.forecast_frame, parsed_forecast)

            self.status_label.config(text=f"Weather data for '{city.strip()}'", fg="green")

        except ValueError as e:
            self.status_label.config(text=str(e), fg="red")
            clear_frame(self.current_frame)
            clear_frame(self.forecast_frame)
        except (requests.ConnectionError, requests.Timeout):
            self.status_label.config(
                text="Connection error. Please check your internet connection.", fg="red")
            clear_frame(self.current_frame)
            clear_frame(self.forecast_frame)
        except requests.RequestException as e:
            self.status_label.config(text=f"Request failed: {e}", fg="red")
            clear_frame(self.current_frame)
            clear_frame(self.forecast_frame)
        except (KeyError, IndexError):
            self.status_label.config(
                text="Error parsing weather data. Unexpected response format.", fg="red")
            clear_frame(self.current_frame)
            clear_frame(self.forecast_frame)


def main():
    """Entry point for the weather application."""
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
