import os
from google import genai
from google.genai import types

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key or api_key == "your_api_key_here":
    print("No valid API key. Skipping test.")
else:
    def get_weather(location: str) -> str:
        """Get the weather for a location."""
        print(f"Tool called: get_weather({location})")
        return f"It is sunny in {location}"

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            tools=[get_weather]
        )
    )
    print("Sending message...")
    response = chat.send_message("What is the weather in Paris?")
    print("Response:", response.text)
