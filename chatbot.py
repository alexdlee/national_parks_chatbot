# chatbot.py
from knowledge_base import parks
from weather import get_current_weather, format_weather_response

def chatbot_response(user_input):
    user_input = user_input.lower()
    for park, details in parks.items():
        if park in user_input:
            highlights = ", ".join(details["highlights"])
            return (f"{park.title()} is located in {details['location']}. "
                    f"Highlights include {highlights}. "
                    f"The best time to visit is {details['best_time']}.")
    
    if "hello" in user_input:
        return "Hi! Welcome to the National Parks Chatbot. How can I assist you today?"
    elif "recommend" in user_input:
        return "I recommend Yellowstone for its geysers and wildlife."
    elif "exit" in user_input:
        return "Goodbye! Have a great trip to the parks!"
    elif "weather" in user_input:
        location = user_input.split("weather in")[-1].strip()
        weather_data = get_current_weather(location)
        return format_weather_response(weather_data)
    else:
        return "I'm not sure how to help with that. Try asking about specific parks!"


def main():
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
