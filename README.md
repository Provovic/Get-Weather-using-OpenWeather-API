To see this code in use, please visit btcloudwebapp.com/weathertracker.

This Azure Function provides current weather information based on a given ZIP code. It utilizes the OpenWeatherMap API to retrieve both the latitude and longitude of the provided ZIP code. These geographical coordinates are then used to make a secondary API call (callAPIGetWeather variable) to gather detailed weather information, including:
  Location Name: The name of the location corresponding to the provided ZIP code.
  Temperature: The current temperature in Fahrenheit.
  Feels Like: The perceived temperature, also in Fahrenheit.
  Humidity: The percentage of humidity in the air.
  Wind Speed: The current wind speed in miles per hour.
  Forecast Summary: A brief description of the weather conditions for the day.
