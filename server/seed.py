from app import app, db
from models.restaurant import Restaurant
from models.pizza import Pizza
from models.restaurant_pizza import RestaurantPizza

def seed_database():
    with app.app_context():
        # Clear existing data
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()

        # Create restaurants
        restaurants = [
            Restaurant(name="Pizza Palace", address="123 Main St"),
            Restaurant(name="Slice of Heaven", address="456 Oak Ave"),
            Restaurant(name="Pizza Paradise", address="789 Pine Rd")
        ]
        db.session.add_all(restaurants)
        db.session.commit()

        # Create pizzas
        pizzas = [
            Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Mozzarella, Basil"),
            Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Mozzarella, Pepperoni"),
            Pizza(name="Vegetarian", ingredients="Dough, Tomato Sauce, Mozzarella, Bell Peppers, Mushrooms, Onions")
        ]
        db.session.add_all(pizzas)
        db.session.commit()

        # Create restaurant_pizzas
        restaurant_pizzas = [
            RestaurantPizza(price=10, restaurant_id=1, pizza_id=1),
            RestaurantPizza(price=12, restaurant_id=1, pizza_id=2),
            RestaurantPizza(price=11, restaurant_id=2, pizza_id=1),
            RestaurantPizza(price=13, restaurant_id=2, pizza_id=3),
            RestaurantPizza(price=12, restaurant_id=3, pizza_id=2),
            RestaurantPizza(price=14, restaurant_id=3, pizza_id=3)
        ]
        db.session.add_all(restaurant_pizzas)
        db.session.commit()

if __name__ == '__main__':
    seed_database() 