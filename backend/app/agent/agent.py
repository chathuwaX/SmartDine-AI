from google import genai
from google.genai import types
import os
from .tools import (
    search_menu,
    recommend_food,
    calculate_order,
    check_table_availability,
    make_reservation,
    get_restaurant_information
)

# Initialize the Gemini Client
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_ID = 'gemini-3.6-flash'

tools = [
    search_menu,
    recommend_food,
    calculate_order,
    check_table_availability,
    make_reservation,
    get_restaurant_information
]

SYSTEM_INSTRUCTION = """You are SmartDine AI, a friendly and helpful restaurant assistant for SmartDine Restaurant.

Your capabilities:
1. Answer general questions about the restaurant conversationally.
2. Search the menu using the search_menu tool.
3. Recommend food using the recommend_food tool.
4. Calculate order totals using the calculate_order tool.
5. Check table availability using the check_table_availability tool.
6. Make reservations using the make_reservation tool (only after checking availability).
7. Provide restaurant information using the get_restaurant_information tool.

Rules:
- For greetings like "hi", "hello", respond warmly WITHOUT using any tools.
- Use tools ONLY when you need specific data (menu items, prices, availability, etc.).
- Never invent food items or prices. Always use tools to get real data.
- Never claim a reservation was made unless the make_reservation tool confirmed it.
- When using calculate_order, format items as: 'Item Name x Quantity, Item Name x Quantity'.
- Be concise and friendly in your responses.
- Use the restaurant's currency: LKR (Sri Lankan Rupees, shown as Rs.).

IMPORTANT formatting rules:
- NEVER use markdown formatting. No #, ##, ###, **, *, or any markdown symbols.
- Use plain text only.
- Use numbered lists (1. 2. 3.) or dashes (- ) for lists.
- Do not use bold or italic formatting.
- Keep responses clean and readable as plain text.
"""


def create_chat_session():
    """Create a new chat session with tools bound."""
    return client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=tools,
            temperature=0.7,
        )
    )
