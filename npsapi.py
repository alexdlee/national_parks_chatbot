import requests

API_KEY = "lCHUhMfqgMNIq7Zlz8YL7eibQLn53EZvqf7wNYUW"
NPS_BASE_URL = "https://developer.nps.gov/api/v1/parks"

def get_park_state_from_nps(park_name):
    """
    Fetch the state code(s) for a national park using the NPS API.

    Args:
        park_name (str): Name of the national park.

    Returns:
        str: State code(s) for the park in ISO 3166 format (e.g., "WY").
    """
    params = {
        "q": park_name,
        "api_key": API_KEY
    }
    response = requests.get(NPS_BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            states = data["data"][0]["states"]  # State codes are returned as a comma-separated string
            return states
        else:
            print(f"No results found for park: {park_name}")
    else:
        print(f"Error fetching data from NPS API: {response.status_code}")
    return None


def fetch_all_parks():
    """
    Fetch all national parks in the USA using the NPS API.

    Returns:
        list: A list of dictionaries, each containing park data.
    """
    BASE_URL = "https://developer.nps.gov/api/v1/parks"
    params = {
        "api_key": API_KEY,
        "limit": 1000  # Fetch up to 1000 parks
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["data"]  # Extract the list of parks
    else:
        print(f"Error: {response.status_code}")
        return []
    

def parse_parks_data(parks_data):
    """
    Parse the raw API data to extract relevant fields for the SQLite database.

    Args:
        parks_data (list): List of dictionaries from the NPS API.

    Returns:
        list: A list of tuples formatted for SQLite insertion.
    """
    parsed_data = []
    for park in parks_data:
        name = park.get("fullName", "Unknown")
        location = park.get("states", "Unknown")
        description = park.get("description", "No description available")
        highlights = ", ".join(activity["name"] for activity in park.get("activities", []))
        best_time = "Data not available"  # The API doesn't provide this; set a default

        # Add the park data as a tuple
        parsed_data.append((name, location, description, highlights, best_time))
    return parsed_data


