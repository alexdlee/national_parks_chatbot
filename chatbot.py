import sqlite3
import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from weather import get_current_weather, format_weather_response, get_uv_index, get_5day_forecast
from utils import fetch_lat_lon_with_openweather, format_location_for_openweather, get_park_state_from_nps, fetch_lat_lon_with_nominatim
from npsapi import get_park_state_from_nps
from collections import defaultdict

# Download NLTK resources
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("stopwords")


# Preprocess user input
def preprocess_input(user_input):
    """
    Tokenize, normalize, and clean user input for better processing.
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    
    # Tokenize and normalize
    tokens = word_tokenize(user_input.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
    
    return tokens

# Query the database for park details
def query_park_from_db(user_tokens):
    """
    Search for a matching park in the database based on user tokens.

    Args:
        user_tokens (list): List of tokens from the user's input.

    Returns:
        tuple: Park details including latitude and longitude if found, otherwise None.
    """
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    for token in user_tokens:
        cursor.execute("""
        SELECT park_id, name, location, description, highlights, best_time 
        FROM parks WHERE name LIKE ?
        """, (f"%{token}%",))
        result = cursor.fetchone()
        if result:
            conn.close()
            return result  # Return the matching park record

    conn.close()
    return None  # No matching park found


# Chatbot response function
def chatbot_response(user_input):
    """
    Generate a chatbot response based on user input.
    """
    # Preprocess the user input
    tokens = preprocess_input(user_input)

    # Check for park details
    park_info = query_park_from_db(tokens)
    if park_info:
        park_id, name, location, description, highlights, best_time = park_info

        # Check if the user is asking about weather
        if "weather" in tokens:
            # Fetch latitude and longitude dynamically
            print(name)
            lat, lon = fetch_lat_lon_with_nominatim(name)
            
            if not lat or not lon:
                return f"Sorry, I couldn't find the location of {name} to fetch weather information."

            # Fetch real-time weather data
            weather_data = get_current_weather(lat, lon)
            if "error" in weather_data:
                return weather_data["error"]

            # Format and return the weather response
            return format_weather_response(weather_data)
        
        if "uv" in tokens:
            lat, lon = fetch_lat_lon_with_nominatim(name)
            print(name)

            if not lat or not lon:
                return f"Sorry, I couldn't find the location of {name} to fetch UV index information."

            # Fetch UV Index
            uv_data = get_uv_index(lat, lon)
            if "error" in uv_data:
                return uv_data["error"]

            uv_index = uv_data.get("value", "unknown")
            return f"The current UV index at {name} is {uv_index}."

        if "forecast" in tokens:
        
            lat, lon = fetch_lat_lon_with_nominatim(name)
            if not lat or not lon:
                return f"Sorry, I couldn't find the location of {name} to fetch weather forecast information."

            # Fetch 5-day forecast
            forecast_data = get_5day_forecast(lat=lat, lon=lon)
            if "error" in forecast_data:
                return forecast_data["error"]

            # Extract the next day's forecast as an example
            daily_forecast = defaultdict(list)

            for entry in forecast_data["list"]:
                date = entry["dt_txt"].split(" ")[0]  # Extract the date (YYYY-MM-DD)
                daily_forecast[date].append(entry)

        # Summarize the forecast for each day
            forecast_summary = []
            for day, entries in daily_forecast.items():
            # Compute average temperature, condition, etc., for the day
                avg_temp = sum(entry["main"]["temp"] for entry in entries) / len(entries)
                condition = entries[0]["weather"][0]["description"].capitalize()
                humidity = sum(entry["main"]["humidity"] for entry in entries) / len(entries)
                wind_speed = sum(entry["wind"]["speed"] for entry in entries) / len(entries)

            # Format the daily forecast
                forecast_summary.append(
                    f"{day}:\n"
                    f"  Temperature: {avg_temp:.1f}°F\n"
                    f"  Condition: {condition}\n"
                    f"  Humidity: {humidity:.1f}%\n"
                    f"  Wind Speed: {wind_speed:.1f} mph"
                )

        # Combine the daily summaries into a single response
            return f"5-Day Forecast for {name}:\n" + "\n\n".join(forecast_summary)

        if "tips" in tokens:
    # Query the park information from the database
            park_info = query_park_from_db(tokens)
            if park_info:
                park_id = park_info[0]  # Extract park_id from the database query
                park_name = park_info[1]

                # Fetch tips for the park
                tips = fetch_tips_for_park(park_id)

                if tips:
                    # Format and return the tips
                    formatted_tips = f"Here are some tips for visiting {park_name}:\n" + "\n".join(
                        f"- {tip}" for tip in tips
                    )
                    return formatted_tips
                else:
                    return f"Sorry, I don't have any tips for {park_name} yet."
            else:
                return "Sorry, I couldn't find the park you mentioned. Please check the name and try again."


        # Otherwise, return park details
        return (f"{name} is located in {location}. "
                f"Highlights include {highlights}. "
                f"The best time to visit is {best_time}. "
                f"Description: {description}")

    # Check for greetings
    if "hello" in tokens:
        return "Hi! Welcome to the National Parks Chatbot. How can I assist you today?"

    # Check for recommendations
    if "recommend" in tokens:
        return recommend_park()

    # Default response
    return "I'm not sure how to help with that. Try asking about specific parks!"



def recommend_park():
    """
    Recommend a random park from the database.
    """
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    # Query all parks
    cursor.execute("SELECT name, highlights FROM parks")
    parks = cursor.fetchall()

    conn.close()

    # Choose a random park to recommend
    if parks:
        park = random.choice(parks)
        return f"I recommend {park[0]}! Highlights include {park[1]}."
    else:
        return "I'm sorry, I couldn't find any parks to recommend right now."


def fetch_tips_for_park(park_id):
    """
    Fetch tips for a specific park from the database.

    Args:
        park_id (int): The ID of the park.

    Returns:
        list: A list of tips for the park, or an empty list if no tips are found.
    """
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    # Query the tips table for the given park_id
    cursor.execute("SELECT tip_text FROM tips WHERE park_id = ?", (park_id,))
    tips = [row[0] for row in cursor.fetchall()]

    conn.close()
    return tips



# Main function to run the chatbot
def main():
    """
    Run the chatbot in a command-line interface.
    """
    print("Welcome to the National Parks Chatbot!")
    print("Type 'exit' to end the chat.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
