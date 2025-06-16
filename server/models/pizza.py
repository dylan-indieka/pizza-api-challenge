"""
This module defines the Pizza model for the Pizza Restaurant API.
It includes fields for pizza details, nutritional info, customization, popularity, and special offers.
"""
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

db = SQLAlchemy()

class Pizza(db.Model):
    """
    SQLAlchemy model for pizzas in the Pizza Restaurant API.
    Includes details such as ingredients, price, nutritional info, customization, popularity, and special offers.
    """
    __tablename__ = 'pizzas'

    # Valid categories and sizes
    VALID_CATEGORIES = ['classic', 'specialty', 'vegetarian', 'vegan', 'gluten-free']
    VALID_SIZES = ['small', 'medium', 'large']
    SIZE_PRICE_MULTIPLIERS = {
        'small': 1.0,
        'medium': 1.5,
        'large': 2.0
    }
    VALID_ALLERGENS = ['dairy', 'eggs', 'fish', 'shellfish', 'tree_nuts', 'peanuts', 'wheat', 'soy']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String)
    category = db.Column(db.String, nullable=False, default='classic')
    size = db.Column(db.String, nullable=False, default='medium')
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    prep_time = db.Column(db.Integer)  # in minutes
    allergens = db.Column(db.String)  # comma-separated list of allergens
    
    # Nutritional information
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)  # in grams
    carbohydrates = db.Column(db.Float)  # in grams
    fat = db.Column(db.Float)  # in grams
    sodium = db.Column(db.Integer)  # in mg
    
    # Customization options (stored as JSON)
    customization_options = db.Column(db.Text)  # JSON string of available customizations
    
    # Popularity tracking
    order_count = db.Column(db.Integer, default=0)
    last_ordered_at = db.Column(db.DateTime)
    
    # Special offers
    is_special = db.Column(db.Boolean, default=False)
    special_price = db.Column(db.Float)
    special_start_date = db.Column(db.DateTime)
    special_end_date = db.Column(db.DateTime)

    # Relationships
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    def get_price_for_size(self, size):
        """
        Calculate the price for a specific size.
        Args:
            size (str): The size of the pizza ('small', 'medium', 'large').
        Returns:
            float: The calculated price for the given size.
        Raises:
            ValueError: If the size is invalid.
        """
        if size not in self.VALID_SIZES:
            raise ValueError(f"Invalid size: {size}")
        return self.price * self.SIZE_PRICE_MULTIPLIERS[size]

    def toggle_availability(self):
        """
        Toggle the availability status of the pizza (available/unavailable).
        """
        self.is_available = not self.is_available

    def update_rating(self, new_rating):
        """
        Update the average rating with a new rating.
        Args:
            new_rating (float): The new rating to add (must be between 0 and 5).
        Raises:
            ValueError: If the new rating is not between 0 and 5.
        """
        if new_rating < 0 or new_rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        
        total_rating = (self.rating * self.rating_count) + new_rating
        self.rating_count += 1
        self.rating = total_rating / self.rating_count

    def get_allergens_list(self):
        """
        Return allergens as a list of strings.
        Returns:
            list: List of allergen names (str) for this pizza.
        """
        return [a.strip() for a in self.allergens.split(',')] if self.allergens else []

    def get_customization_options(self):
        """
        Return customization options as a dictionary.
        Returns:
            dict: Customization options for this pizza.
        """
        if not self.customization_options:
            return {}
        return json.loads(self.customization_options)

    def set_customization_options(self, options):
        """
        Set customization options from a dictionary.
        Args:
            options (dict): Customization options to set.
        Raises:
            ValueError: If options is not a dictionary.
        """
        if not isinstance(options, dict):
            raise ValueError("Customization options must be a dictionary")
        self.customization_options = json.dumps(options)

    def increment_order_count(self):
        """
        Increment the order count and update the last ordered timestamp for this pizza.
        """
        self.order_count += 1
        self.last_ordered_at = datetime.utcnow()

    def get_current_price(self):
        """
        Get the current price considering any active special offers.
        Returns:
            float: The current price (special price if active, otherwise regular price).
        """
        if self.is_special and self.special_price is not None:
            now = datetime.utcnow()
            if (self.special_start_date is None or now >= self.special_start_date) and \
               (self.special_end_date is None or now <= self.special_end_date):
                return self.special_price
        return self.price

    def get_discount_percentage(self):
        """
        Calculate the discount percentage for active special offers.
        Returns:
            float: The discount percentage if a special offer is active, otherwise 0.0.
        """
        if self.is_special and self.special_price is not None:
            now = datetime.utcnow()
            if (self.special_start_date is None or now >= self.special_start_date) and \
               (self.special_end_date is None or now <= self.special_end_date):
                return round(((self.price - self.special_price) / self.price) * 100, 2)
        return 0.0

    def set_special_offer(self, special_price, start_date=None, end_date=None):
        """Set a special offer for the pizza"""
        if special_price >= self.price:
            raise ValueError("Special price must be less than regular price")
        self.is_special = True
        self.special_price = special_price
        self.special_start_date = start_date
        self.special_end_date = end_date

    def end_special_offer(self):
        """End the current special offer"""
        self.is_special = False
        self.special_price = None
        self.special_start_date = None
        self.special_end_date = None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'price': self.get_current_price(),
            'original_price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'size': self.size,
            'is_available': self.is_available,
            'rating': self.rating,
            'rating_count': self.rating_count,
            'prep_time': self.prep_time,
            'allergens': self.get_allergens_list(),
            'nutritional_info': {
                'calories': self.calories,
                'protein': self.protein,
                'carbohydrates': self.carbohydrates,
                'fat': self.fat,
                'sodium': self.sodium
            },
            'customization_options': self.get_customization_options(),
            'popularity': {
                'order_count': self.order_count,
                'last_ordered_at': self.last_ordered_at.isoformat() if self.last_ordered_at else None
            },
            'special_offer': {
                'is_special': self.is_special,
                'special_price': self.special_price,
                'special_start_date': self.special_start_date.isoformat() if self.special_start_date else None,
                'special_end_date': self.special_end_date.isoformat() if self.special_end_date else None
            }
        } 