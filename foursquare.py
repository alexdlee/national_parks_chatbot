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

    print(response.text)
    if response.status_code == 200:
        return response.json()  # Returns places data as a dictionary
    else:
        return {"error": f"Failed to fetch parks data: {response.status_code}"}


# fetch_nearby_places(44.5979, -110.5612) # sample call




def get_fsq_id(query, near=None, lat=None, lon=None):
    """
    Search for a place by name and return its fsq_id.

    Args:
        query (str): The name of the location to search for.
        near (str): An optional city/area to narrow the search.
        lat (float): Optional latitude of the location.
        lon (float): Optional longitude of the location.

    Returns:
        str: The fsq_id of the location if found, or None.
    """
    BASE_URL = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": API_KEY
    }
    params = {
        "query": query,
        "limit": 1  # Get only the top result
    }

    # Add optional parameters
    if near:
        params["near"] = near
    if lat and lon:
        params["ll"] = f"{lat},{lon}"
    
    # Make the API request
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            # Return the fsq_id of the first result
            return data["results"][0]["fsq_id"]
        else:
            print("No results found.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example Usage
fsq_id = get_fsq_id(query="Yellowstone National Park", lat=44.4280, lon=-110.5885)
# print(f"Foursquare ID: {fsq_id}")




def fetch_place_tips(fsq_id):
    BASE_URL = f"https://api.foursquare.com/v3/places/{fsq_id}/tips"

    headers = {
        "Authorization": API_KEY
    }

    params = {
        "limit": 20
    }

    response = requests.get(BASE_URL, headers=headers)

    print(response.text)


fetch_place_tips(fsq_id)


