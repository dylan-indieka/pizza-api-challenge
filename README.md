# Pizza Restaurant API

A RESTful API for managing pizza restaurants, pizzas, and their relationships.

## Project Structure (MVC Pattern)

```
.
├── server/
│   ├── __init__.py
│   ├── app.py                # App setup
│   ├── config.py             # DB config
│   ├── models/               # Data layer
│   │   ├── __init__.py
│   │   ├── restaurant.py
│   │   ├── pizza.py
│   │   └── restaurant_pizza.py
│   ├── controllers/          # Route handlers
│   │   ├── __init__.py
│   │   ├── restaurant_controller.py
│   │   ├── pizza_controller.py
│   │   └── restaurant_pizza_controller.py
│   └── seed.py              # Seed data
├── migrations/
└── README.md
```

## Setup Instructions

1. Create and activate virtual environment:
```bash
pipenv install flask flask_sqlalchemy flask_migrate
pipenv shell
```

2. Set up the database:
```bash
# Set Flask application
export FLASK_APP=server/app.py

# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

3. Seed the database:
```bash
python server/seed.py
```

4. Run the application:
```bash
python server/app.py
```

The server will start on http://localhost:5555

## API Endpoints & Examples

### Restaurants

#### GET /restaurants
Returns a list of all restaurants.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Pizza Palace",
    "address": "123 Main St"
  },
  {
    "id": 2,
    "name": "Slice of Heaven",
    "address": "456 Oak Ave"
  }
]
```

#### GET /restaurants/<id>
Returns a specific restaurant with its pizzas.

**Response:**
```json
{
  "id": 1,
  "name": "Pizza Palace",
  "address": "123 Main St",
  "pizzas": [
    {
      "id": 1,
      "name": "Margherita",
      "ingredients": "Dough, Tomato Sauce, Mozzarella, Basil"
    },
    {
      "id": 2,
      "name": "Pepperoni",
      "ingredients": "Dough, Tomato Sauce, Mozzarella, Pepperoni"
    }
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Restaurant not found"
}
```

#### DELETE /restaurants/<id>
Deletes a restaurant and its associated restaurant pizzas.

**Success Response:**
- Status Code: 204 No Content

**Error Response (404):**
```json
{
  "error": "Restaurant not found"
}
```

### Pizzas

#### GET /pizzas
Returns a list of all pizzas.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Margherita",
    "ingredients": "Dough, Tomato Sauce, Mozzarella, Basil"
  },
  {
    "id": 2,
    "name": "Pepperoni",
    "ingredients": "Dough, Tomato Sauce, Mozzarella, Pepperoni"
  }
]
```

### Restaurant Pizzas

#### POST /restaurant_pizzas
Creates a new restaurant pizza.

**Request Body:**
```json
{
  "price": 10,
  "pizza_id": 1,
  "restaurant_id": 1
}
```

**Success Response:**
```json
{
  "id": 1,
  "price": 10,
  "pizza_id": 1,
  "restaurant_id": 1,
  "pizza": {
    "id": 1,
    "name": "Margherita",
    "ingredients": "Dough, Tomato Sauce, Mozzarella, Basil"
  },
  "restaurant": {
    "id": 1,
    "name": "Pizza Palace",
    "address": "123 Main St"
  }
}
```

**Error Response (400):**
```json
{
  "errors": ["Price must be between 1 and 30"]
}
```

## Validation Rules

1. RestaurantPizza:
   - Price must be between 1 and 30
   - Both pizza_id and restaurant_id must exist
   - All fields are required

2. Restaurant:
   - Name and address are required
   - Cascading delete for associated RestaurantPizzas

3. Pizza:
   - Name and ingredients are required

## Testing with Postman

1. Import the Postman Collection:
   - Open Postman
   - Click "Import" button
   - Select the `challenge-1-pizzas.postman_collection.json` file

2. Test Each Endpoint:
   - GET /restaurants
   - GET /restaurants/<id>
   - DELETE /restaurants/<id>
   - GET /pizzas
   - POST /restaurant_pizzas

3. Example Test Cases:
   - Create a restaurant pizza with valid price (1-30)
   - Create a restaurant pizza with invalid price (>30)
   - Get a non-existent restaurant
   - Delete a restaurant and verify associated pizzas are removed

## Error Handling

The API returns appropriate error messages and status codes:
- 404: Resource not found
- 400: Invalid request data
- 204: Successful deletion
- 201: Successful creation 