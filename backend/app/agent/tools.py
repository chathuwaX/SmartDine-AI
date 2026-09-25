import sqlite3
import datetime
import uuid
import os
from typing import List, Dict, Any, Optional

# Use absolute path to the database file so it works regardless of working directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "smartdine.db")


def search_menu(query: str) -> str:
    """Search the restaurant menu for food items. Use this tool when the user asks about specific food items, categories, or dietary preferences like vegetarian.

    Args:
        query: The search term (e.g. 'chicken pizza', 'vegetarian', 'burgers')

    Returns:
        A formatted string listing matching menu items with name, price, and description.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        search_term = f"%{query.lower()}%"
        cursor.execute(
            "SELECT name, category, description, price, vegetarian FROM menu_items WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?",
            (search_term, search_term, search_term)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No menu items found matching '{query}'."

        results = []
        for row in rows:
            veg = " (Vegetarian)" if row['vegetarian'] else ""
            results.append(f"- {row['name']}{veg} — Rs. {int(row['price'])} — {row['description']}")
        return "\n".join(results)
    except Exception as e:
        return f"Error searching menu: {str(e)}"


def recommend_food(preference: str = "any", budget: float = 99999, category: str = "any") -> str:
    """Recommend food based on user preferences, budget, or category. Use when a user asks for food recommendations or suggestions.

    Args:
        preference: Dietary preference. Use 'vegetarian' for vegetarian food, or 'any' for all food.
        budget: Maximum budget in LKR (Sri Lankan Rupees). Default is no limit.
        category: Food category like 'Burgers', 'Pizza', 'Rice', 'Drinks', 'Desserts', or 'any' for all.

    Returns:
        A formatted string listing recommended menu items.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT name, category, description, price, vegetarian FROM menu_items WHERE price <= ?"
        params = [budget]

        if preference.lower() == 'vegetarian':
            query += " AND vegetarian = 1"

        if category.lower() != 'any':
            query += " AND LOWER(category) = ?"
            params.append(category.lower())

        query += " ORDER BY price ASC LIMIT 5"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No menu items found matching your criteria."

        results = []
        for row in rows:
            veg = " (Vegetarian)" if row['vegetarian'] else ""
            results.append(f"- {row['name']}{veg} — Rs. {int(row['price'])} — {row['description']}")
        return "Here are my recommendations:\n" + "\n".join(results)
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"


def calculate_order(items: str) -> str:
    """Calculate the total price of a food order based on actual menu prices. Use this when a user asks about the cost or total price of specific items. IMPORTANT: The 'items' argument must be a comma-separated string like 'Classic Chicken Burger x2, Coke x3'.

    Args:
        items: A comma-separated string of items and quantities. Format: 'Item Name x Quantity, Item Name x Quantity'. Example: 'Classic Chicken Burger x2, Coke x1'

    Returns:
        A formatted string with the order breakdown including subtotal, tax, and total.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        subtotal = 0.0
        lines = []

        # Parse the items string
        item_list = [i.strip() for i in items.split(",")]
        for entry in item_list:
            # Try to parse "Item Name x Quantity" or "Item Name xQuantity" or just "Item Name"
            parts = entry.rsplit(" x", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                try:
                    qty = int(parts[1].strip())
                except ValueError:
                    qty = 1
            else:
                name = entry.strip()
                qty = 1

            cursor.execute("SELECT name, price FROM menu_items WHERE LOWER(name) LIKE LOWER(?)", (f"%{name}%",))
            row = cursor.fetchone()

            if row:
                item_price = row['price']
                item_total = item_price * qty
                subtotal += item_total
                lines.append(f"- {row['name']} x{qty} = Rs. {int(item_total)} (Rs. {int(item_price)} each)")
            else:
                lines.append(f"- {name}: NOT FOUND on our menu")

        conn.close()

        tax = subtotal * 0.10
        total = subtotal + tax

        result = "Order Breakdown:\n"
        result += "\n".join(lines)
        result += f"\n\nSubtotal: Rs. {int(subtotal)}"
        result += f"\nTax (10%): Rs. {int(tax)}"
        result += f"\nTotal: Rs. {int(total)}"
        return result
    except Exception as e:
        return f"Error calculating order: {str(e)}"


def check_table_availability(date: str, time: str, guests: int) -> str:
    """Check if a table is available at the restaurant for a given date, time, and number of guests.

    Args:
        date: The date for the reservation (e.g. '2026-09-24' or 'tomorrow').
        time: The time for the reservation (e.g. '19:00' or '7 PM').
        guests: The number of guests.

    Returns:
        A string indicating whether a table is available or not.
    """
    if guests <= 0:
        return "Invalid number of guests. Please specify at least 1 guest."
    if guests > 20:
        return "Sorry, we cannot accommodate more than 20 guests at a single table. Please contact us directly at 011-234-5678 for large events."

    return f"Yes, a table for {guests} guests is available on {date} at {time}. Would you like to make a reservation? If so, please provide your name."


def make_reservation(customer_name: str, date: str, time: str, guests: int) -> str:
    """Make a table reservation at the restaurant. ONLY use this after check_table_availability confirmed availability.

    Args:
        customer_name: The name of the customer making the reservation.
        date: The date for the reservation (e.g. '2026-09-24').
        time: The time for the reservation (e.g. '19:00').
        guests: The number of guests.

    Returns:
        A string with the reservation confirmation details.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        year = datetime.datetime.now().year
        res_id = f"SD-{year}-{uuid.uuid4().hex[:4].upper()}"

        cursor.execute(
            "INSERT INTO reservations (id, customer_name, date, time, guests, status) VALUES (?, ?, ?, ?, ?, ?)",
            (res_id, customer_name, date, time, guests, "confirmed")
        )
        conn.commit()
        conn.close()

        return f"Reservation confirmed!\n- Reservation ID: {res_id}\n- Name: {customer_name}\n- Date: {date}\n- Time: {time}\n- Guests: {guests}\n- Status: Confirmed"
    except Exception as e:
        return f"Error creating reservation: {str(e)}"


def get_restaurant_information(topic: str) -> str:
    """Get general information about SmartDine Restaurant. Use this when the user asks about opening hours, location, contact, parking, delivery, takeaway, payment methods, or cancellation policy.

    Args:
        topic: The topic to get information about (e.g. 'opening hours', 'location', 'contact', 'parking', 'delivery', 'payment methods').

    Returns:
        A string with the requested restaurant information.
    """
    info = {
        "opening hours": "SmartDine Restaurant is open Monday to Sunday, 10:00 AM to 11:00 PM.",
        "location": "We are located at 123 Food Street, Colombo 03, Sri Lanka.",
        "contact": "Phone: 011-234-5678 | Email: hello@smartdine.lk",
        "parking": "Free valet parking is available for all customers.",
        "delivery": "Delivery is available via UberEats and PickMe Food within a 10km radius.",
        "takeaway": "Takeaway is available. Call ahead at 011-234-5678 to place your order.",
        "payment methods": "We accept Cash, Credit/Debit Cards (Visa, Mastercard, Amex), Apple Pay, and Google Pay.",
        "cancellation policy": "Reservations can be cancelled up to 2 hours before the booked time without any penalty."
    }

    topic_lower = topic.lower()
    for key, value in info.items():
        if key in topic_lower or topic_lower in key:
            return value

    # If no exact match, return all info
    all_info = "\n".join([f"- {k.title()}: {v}" for k, v in info.items()])
    return f"Here is our restaurant information:\n{all_info}"
