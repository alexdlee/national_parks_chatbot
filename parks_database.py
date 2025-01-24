import sqlite3
from foursquare import fetch_nearby_places, fetch_place_tips, get_fsq_id
from npsapi import fetch_all_parks, parse_parks_data
from weather import get_current_weather, get_5day_forecast, get_uv_index, format_weather_response

def create_tables():
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parks (
        park_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        description TEXT,
        highlights TEXT,
        best_time TEXT
    )
    """)

    # Create the tips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tips (
        tip_id INTEGER PRIMARY KEY AUTOINCREMENT,
        park_id INTEGER,
        tip_text TEXT,
        FOREIGN KEY (park_id) REFERENCES parks(park_id)
    )
    """)

    # Create the nearby_places table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nearby_places (
        place_id INTEGER PRIMARY KEY AUTOINCREMENT,
        park_id INTEGER,
        name TEXT,
        address TEXT,
        category TEXT,
        distance INTEGER,
        FOREIGN KEY (park_id) REFERENCES parks(park_id)
    )
    """)


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()

def insert_parks_into_db(parsed_parks):
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT INTO parks (name, location, description, highlights, best_time)
    VALUES (?, ?, ?, ?, ?)
    """, parsed_parks)

    # Get all park_ids with their names for association
    cursor.execute("SELECT park_id, name FROM parks")
    parks_mapping = {row[1]: row[0] for row in cursor.fetchall()}

    conn.commit()
    conn.close()
    return parks_mapping  # Map of park_name -> park_id

def insert_tips_into_db(park_id, tips):
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    tip_data = [(park_id, tip["text"]) for tip in tips]
    cursor.executemany("""
    INSERT INTO tips (park_id, tip_text)
    VALUES (?, ?)
    """, tip_data)

    conn.commit()
    conn.close()

def insert_nearby_places_into_db(park_id, places):
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    place_data = [
        (park_id, place["name"], place["location"].get("address", "No address"),
         place["categories"][0]["name"] if place["categories"] else "Unknown", place["distance"])
        for place in places
    ]

    cursor.executemany("""
    INSERT INTO nearby_places (park_id, name, address, category, distance)
    VALUES (?, ?, ?, ?, ?)
    """, place_data)

    conn.commit()
    conn.close()



def main():
    # Step 1: Fetch and parse parks data from NPS API
    parks_data = fetch_all_parks()
    if not parks_data:
        print("No parks data found. Exiting.")
        return

    parsed_parks = parse_parks_data(parks_data)

    # Step 2: Insert parks into the database and get park_id mappings
    parks_mapping = insert_parks_into_db(parsed_parks)

    # Step 3: For each park, fetch and insert tips and nearby places
    for park in parks_data:
        park_name = park["fullName"]
        lat, lon = park["latitude"], park["longitude"]

        # Get the park_id from the mapping
        park_id = parks_mapping.get(park_name)
        fsq_id = get_fsq_id(park_name, lat, lon)

        if not fsq_id:
            continue

        # Fetch and insert tips
        try:
            tips = fetch_place_tips(fsq_id)
            if tips:
                insert_tips_into_db(park_id, tips)
        except Exception as e:
            print(f"Error fetching tips for {park_name}: {e}")

        # Fetch and insert nearby places
        try:
            nearby_places = fetch_nearby_places(lat, lon)
            if nearby_places:
                insert_nearby_places_into_db(park_id, nearby_places)
        except Exception as e:
            print(f"Error fetching nearby places for {park_name}: {e}")

# Run the workflow
if __name__ == "__main__":
    main()

