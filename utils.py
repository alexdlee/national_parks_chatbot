import requests

from npsapi import get_park_state_from_nps

# API keys
NPS_API_KEY = "lCHUhMfqgMNIq7Zlz8YL7eibQLn53EZvqf7wNYUW"
OPENWEATHER_API_KEY = "a92b15c4f52c422e359de572846c8cfb"

def format_location_for_openweather(name):
    """
    Format the location string to match OpenWeather's required format,
    using the NPS API to fetch the state code dynamically.

    Args:
        name (str): Name of the park.

    Returns:
        str: Formatted location string.
    """
    state_code = get_park_state_from_nps(name)  # Fetch state code dynamically
    if state_code:
        return f"{name}, {state_code}, US"
    return f"{name}, US"  # Fallback if state code isn't found

def fetch_lat_lon_with_openweather(location_name):
    """
    Fetch latitude and longitude for a location using OpenWeatherMap Geocoding API.

    Args:
        location_name (str): The name of the location (e.g., "Yellowstone National Park").

    Returns:
        tuple: (latitude, longitude) if found, otherwise (None, None).
    """
    formatted_location = format_location_for_openweather(location_name)
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": formatted_location,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
        else:
            print(f"No results found for location: {formatted_location}")
    else:
        print(f"Error fetching geocoding data: {response.status_code}")
    return None, None

import requests
import time

def fetch_lat_lon_with_nominatim(location_name):
    """
    Fetch latitude and longitude for a location using the Nominatim (OpenStreetMap) Search API.

    Args:
        location_name (str): The name of the location (e.g., "Yellowstone National Park").

    Returns:
        tuple: (latitude, longitude) if found, otherwise (None, None).
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,      # The query string (e.g., park name)
        "format": "json",        # Request JSON-formatted results
        "addressdetails": 1,     # Include detailed address components
        "limit": 1               # Only return the top result
    }
    headers = {
        "User-Agent": "NationalParksChatbot/1.0 (alexdnl@umich.edu)"  # Replace with a valid email address
    }
    
    # Adhere to Nominatim rate limit
    time.sleep(1)  # Wait 1 second before making the request

    # Make the API request
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]["lat"])  # Extract latitude
            lon = float(data[0]["lon"])  # Extract longitude
            return lat, lon
        else:
            print(f"No results found for location: {location_name}")
    else:
        print(f"Error fetching geocoding data: {response.status_code}")
    return None, None


 
