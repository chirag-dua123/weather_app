"""Unit tests for weather_data module."""

import unittest
from unittest.mock import patch, MagicMock
from weather_data import (
    validate_input,
    parse_current_weather,
    parse_forecast,
    fetch_current_weather,
    fetch_forecast,
)


class TestValidateInput(unittest.TestCase):
    """Tests for the validate_input function."""

    def test_empty_string(self):
        valid, msg = validate_input("")
        self.assertFalse(valid)
        self.assertIn("enter a city name", msg.lower())

    def test_whitespace_only(self):
        valid, msg = validate_input("   ")
        self.assertFalse(valid)

    def test_none_input(self):
        valid, msg = validate_input(None)
        self.assertFalse(valid)

    def test_valid_city(self):
        valid, msg = validate_input("London")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_valid_city_with_spaces(self):
        valid, msg = validate_input("New York")
        self.assertTrue(valid)

    def test_valid_city_with_hyphen(self):
        valid, msg = validate_input("Stratford-upon-Avon")
        self.assertTrue(valid)

    def test_invalid_characters(self):
        valid, msg = validate_input("London123")
        self.assertFalse(valid)
        self.assertIn("invalid characters", msg.lower())


class TestParseCurrentWeather(unittest.TestCase):
    """Tests for the parse_current_weather function."""

    def test_parse_valid_response(self):
        data = {
            "main": {"temp": 20.5, "humidity": 65},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 3.2}
        }
        result = parse_current_weather(data)
        self.assertEqual(result["temperature"], "20.5 °C")
        self.assertEqual(result["condition"], "Clear Sky")
        self.assertEqual(result["humidity"], "65%")
        self.assertEqual(result["wind_speed"], "3.2 m/s")

    def test_parse_negative_temp(self):
        data = {
            "main": {"temp": -5.0, "humidity": 80},
            "weather": [{"description": "snow"}],
            "wind": {"speed": 1.0}
        }
        result = parse_current_weather(data)
        self.assertEqual(result["temperature"], "-5.0 °C")

    def test_parse_missing_key_raises(self):
        data = {"main": {"temp": 20}}
        with self.assertRaises(KeyError):
            parse_current_weather(data)


class TestParseForecast(unittest.TestCase):
    """Tests for the parse_forecast function."""

    def test_parse_single_day(self):
        data = {
            "list": [
                {
                    "dt_txt": "2026-02-07 12:00:00",
                    "main": {"temp": 10.0},
                    "weather": [{"description": "clouds"}]
                },
                {
                    "dt_txt": "2026-02-07 15:00:00",
                    "main": {"temp": 12.0},
                    "weather": [{"description": "clouds"}]
                }
            ]
        }
        result = parse_forecast(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["max_temp"], "12.0 °C")
        self.assertEqual(result[0]["min_temp"], "10.0 °C")
        self.assertEqual(result[0]["condition"], "Clouds")

    def test_parse_multiple_days(self):
        data = {
            "list": [
                {
                    "dt_txt": "2026-02-07 12:00:00",
                    "main": {"temp": 10.0},
                    "weather": [{"description": "rain"}]
                },
                {
                    "dt_txt": "2026-02-08 12:00:00",
                    "main": {"temp": 15.0},
                    "weather": [{"description": "clear sky"}]
                }
            ]
        }
        result = parse_forecast(data)
        self.assertEqual(len(result), 2)

    def test_parse_empty_list(self):
        data = {"list": []}
        result = parse_forecast(data)
        self.assertEqual(result, [])


class TestFetchCurrentWeather(unittest.TestCase):
    """Tests for the fetch_current_weather function."""

    @patch("weather_data.API_KEY", "test_key")
    @patch("weather_data.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"main": {"temp": 20}}
        mock_get.return_value = mock_response

        result = fetch_current_weather("London")
        self.assertEqual(result["main"]["temp"], 20)

    @patch("weather_data.API_KEY", "test_key")
    @patch("weather_data.requests.get")
    def test_city_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as ctx:
            fetch_current_weather("InvalidCity")
        self.assertIn("not found", str(ctx.exception))

    @patch("weather_data.API_KEY", "test_key")
    @patch("weather_data.requests.get")
    def test_invalid_api_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as ctx:
            fetch_current_weather("London")
        self.assertIn("Invalid API key", str(ctx.exception))

    @patch("weather_data.API_KEY", None)
    def test_missing_api_key(self):
        with self.assertRaises(ValueError) as ctx:
            fetch_current_weather("London")
        self.assertIn("missing", str(ctx.exception).lower())

    @patch("weather_data.API_KEY", "test_key")
    @patch("weather_data.requests.get")
    def test_server_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(ConnectionError):
            fetch_current_weather("London")


class TestFetchForecast(unittest.TestCase):
    """Tests for the fetch_forecast function."""

    @patch("weather_data.API_KEY", "test_key")
    @patch("weather_data.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"list": []}
        mock_get.return_value = mock_response

        result = fetch_forecast("London")
        self.assertEqual(result["list"], [])

    @patch("weather_data.API_KEY", None)
    def test_missing_api_key(self):
        with self.assertRaises(ValueError):
            fetch_forecast("London")


if __name__ == "__main__":
    unittest.main()
