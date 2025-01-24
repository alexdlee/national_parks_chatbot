import requests

API_KEY = "fsq3zKxTeu13nwBKPpsP3oViXFtpwcweAJI/Y4f8vWfmpTs="

def fetch_nearby_places(lat, lon):
    BASE_URL = "https://api.foursquare.com/v3/places/search"
    ll = str(lat) + "," + str(lon)
    headers = {
        "Authorization": API_KEY
    }

    params = {
        "ll": ll,
        "radius": 16094,
        "limit": 15
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["results"]


# fetch_nearby_places(44.5979, -110.5612) # sample call


import requests

def get_fsq_id(park_name, lat, lon):
    """
    Fetch the Foursquare ID (fsq_id) for a place using latitude and longitude.

    Args:
        park_name (str): Name of the park (used for debugging purposes).
        lat (float): Latitude of the park.
        lon (float): Longitude of the park.

    Returns:
        str: Foursquare ID (fsq_id) of the place if found, otherwise None.
    """
    BASE_URL = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": API_KEY
    }
    params = {
        "ll": f"{lat},{lon}",  # Latitude and longitude
        # "query": park_name,    # Use park name for more accurate results
        "limit": 1             # Get only the top result
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Check if results are available
        if data["results"]:
            return data["results"][0]["fsq_id"]  # Return the fsq_id of the first result

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Foursquare ID for {park_name}: {e}")
        return None



def fetch_place_tips(fsq_id):
    BASE_URL = f"https://api.foursquare.com/v3/places/{fsq_id}/tips"

    headers = {
        "Authorization": API_KEY
    }

    params = {
        "limit": 15
    }

    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        return response.json()



