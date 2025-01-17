import requests

API_KEY = "a92b15c4f52c422e359de572846c8cfb"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_current_weather(location):
    params = {
        "lat": -40,      # Latitude (placeholder)
        "lon": -40,     # Longitude (placeholder)
        "appid": API_KEY,     # API Key
        "units": "metric"     # Use "imperial" for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()  # Returns weather data as a dictionary
    else:
        return {"error": f"Failed to fetch weather data: {response.status_code}"}


def get_uv_index(lat, lon):
    BASE_URL = "http://api.openweathermap.org/data/2.5/uvi"
    params = {
        "lat": -40,
        "lon": 40,
        "appid": API_KEY,
        "units": "metric" 
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch UV Index: {response.status_code}"}
    

def get_5day_forecast(location):
    BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
       "lat": -40,
        "lon": 40,
        "appid": API_KEY,
        "units": "metric" 
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch 5-day forecast: {response.status_code}"}


def format_weather_response(data):
    if "error" in data:
        return data["error"]
    
    location = data["name"]
    temperature = data["main"]["temp"]
    weather_description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    return (
        f"Weather in {location}:\n"
        f"Temperature: {temperature}°C\n"
        f"Condition: {weather_description.capitalize()}\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )


