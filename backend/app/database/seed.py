from sqlalchemy.orm import Session
from .models import MenuItem, Base
from .database import engine

def seed_database(db: Session):
    Base.metadata.create_all(bind=engine)
    
    # Check if we already have data
    if db.query(MenuItem).first():
        return
        
    menu_items = [
        # Burgers
        {"name": "Classic Chicken Burger", "category": "Burgers", "description": "Grilled chicken patty with fresh lettuce and mayo", "price": 1200, "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Crispy Chicken Burger", "category": "Burgers", "description": "Crispy fried chicken with cheese and spicy sauce", "price": 1500, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Beef Cheese Burger", "category": "Burgers", "description": "Juicy beef patty with double cheese", "price": 1800, "image_url": "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Veggie Burger", "category": "Burgers", "description": "Plant-based patty with fresh veggies", "price": 1000, "image_url": "https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400&h=300&fit=crop", "vegetarian": True},
        
        # Pizza
        {"name": "Margherita Pizza", "category": "Pizza", "description": "Classic tomato and mozzarella cheese", "price": 1800, "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Chicken BBQ Pizza", "category": "Pizza", "description": "BBQ chicken, onions, and cheese", "price": 2500, "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Pepperoni Pizza", "category": "Pizza", "description": "Beef pepperoni and extra cheese", "price": 2600, "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Vegetable Pizza", "category": "Pizza", "description": "Assorted vegetables with olives and cheese", "price": 2000, "image_url": "https://images.unsplash.com/photo-1528137871618-79d2761e3fd5?w=400&h=300&fit=crop", "vegetarian": True},
        
        # Rice
        {"name": "Chicken Fried Rice", "category": "Rice", "description": "Wok-tossed rice with chicken and vegetables", "price": 1200, "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Seafood Fried Rice", "category": "Rice", "description": "Fried rice with prawns and cuttlefish", "price": 1600, "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400&h=300&fit=crop", "vegetarian": False},
        {"name": "Vegetable Fried Rice", "category": "Rice", "description": "Fried rice with mixed seasonal vegetables", "price": 900, "image_url": "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Sri Lankan Chicken Rice", "category": "Rice", "description": "Authentic rice with chicken curry and sambal", "price": 1400, "image_url": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop", "vegetarian": False},
        
        # Drinks
        {"name": "Coke", "category": "Drinks", "description": "Chilled Coca-Cola", "price": 300, "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Sprite", "category": "Drinks", "description": "Chilled Sprite", "price": 300, "image_url": "https://images.unsplash.com/photo-1625772299848-391b6a518456?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Fresh Orange Juice", "category": "Drinks", "description": "Freshly squeezed orange juice", "price": 600, "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Mango Juice", "category": "Drinks", "description": "Fresh mango juice", "price": 650, "image_url": "https://images.unsplash.com/photo-1622597467836-f38240662c8c?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Mineral Water", "category": "Drinks", "description": "Bottled mineral water", "price": 150, "image_url": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=400&h=300&fit=crop", "vegetarian": True},
        
        # Desserts
        {"name": "Chocolate Cake", "category": "Desserts", "description": "Rich chocolate cake slice", "price": 700, "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Ice Cream", "category": "Desserts", "description": "Two scoops of vanilla or chocolate ice cream", "price": 500, "image_url": "https://images.unsplash.com/photo-1570197781417-0a5f9be28f14?w=400&h=300&fit=crop", "vegetarian": True},
        {"name": "Brownie", "category": "Desserts", "description": "Warm chocolate brownie with walnuts", "price": 800, "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400&h=300&fit=crop", "vegetarian": True},
    ]

    for item in menu_items:
        db_item = MenuItem(**item)
        db.add(db_item)
    
    db.commit()
