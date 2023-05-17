"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Change, Order, FoodItem, StoreItem, AquaticItem, OrderItem
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    # Get all users from the database.
    with db.session as session:
        users = session.query(User).all()

    # Return a JSON response with the users.
    return jsonify([user.serialize() for user in users]), 200

@app.route('/changes', methods=['POST'])
def register_change():
    # Get the user name, change type, and change data from the request body.
    user_name = request.json['user_name']
    change_type = request.json['change_type']
    change_data = request.json['change_data']

    # Insert a new row into the `changes` table.
    with db.session as session:
        change = Change(
            timestamp=datetime.now(),
            user_name=user_name,
            change_type=change_type,
            change_data=change_data,
        )
        session.add(change)
        session.commit()

    # Return a success message.
    return jsonify({'message': 'Change registered successfully'}), 201



@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Get the user with the specified ID from the database.
    with db.session as session:
        user = session.query(User).get(user_id)

    # Return a JSON response with the user.
    return jsonify(user.serialize()), 200

@app.route('/users', methods=['POST'])
def create_user():
    # Get the user data from the request body.
    user_data = request.json

    # Create a new user object.
    user = User(
        name=user_data['name'],
        role=user_data['role'],
        date_of_birth=user_data['date_of_birth'],
        user_name=user_data['user_name'],
        password=user_data['password'],
    )

    # Add the user to the database.
    with db.session as session:
        session.add(user)
        session.commit()

    # Return a success message.
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Get the user data from the request body.
    user_data = request.json

    # Get the user with the specified ID from the database.
    with db.session as session:
        user = session.query(User).get(user_id)

    # Update the user's data.
    user.name = user_data['name']
    user.role = user_data['role']
    user.date_of_birth = user_data['date_of_birth']
    user.user_name = user_data['user_name']
    user.password = user_data['password']

    # Commit the changes to the database.
    session.commit()

    # Return a success message.
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Get the user with the specified ID from the database.
    with db.session as session:
        user = session.query(User).get(user_id)

    # Delete the user from the database.
    session.delete(user)
    session.commit()

    # Return a success message.
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/orders', methods=['GET'])
def get_orders():
    # Get all orders from the database.
    with db.session as session:
        orders = session.query(Order).all()

    # Return a JSON response with the orders.
    return jsonify([order.serialize() for order in orders]), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Get the order with the specified ID from the database.
    with db.session as session:
        order = session.query(Order).get(order_id)

    # Return a JSON response with the order.
    return jsonify(order.serialize()), 200

@app.route('/orders', methods=['POST'])
def create_order():
    # Get the order data from the request body.
    order_data = request.json

    # Create a new order object.
    order = Order(
        table_number=order_data['table_number'],
        number_of_people=order_data['number_of_people'],
    )

    # Add the order to the database.
    with db.session as session:
        session.add(order)
        session.commit()

    # Return a success message.
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    # Get the order data from the request body.
    order_data = request.json

    # Get the order with the specified ID from the database.
    with db.session as session:
        order = session.query(Order).get(order_id)

    # Update the order's data.
    order.table_number = order_data['table_number']
    order.number_of_people = order_data['number_of_people']

    # Commit the changes to the database.
    session.commit()

    # Return a success message.
    return jsonify({'message': 'Order updated successfully'}), 200


# Order routes
@app.route('/orders', methods=['GET'])
def get_orders():
    with db.session as session:
        orders = session.query(Order).all()
    return jsonify([order.serialize() for order in orders]), 200

@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    order = Order(table_number=order_data['table_number'], number_of_people=order_data['number_of_people'])
    with db.session as session:
        session.add(order)
        session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order_data = request.json
    with db.session as session:
        order = session.query(Order).get(order_id)
        order.table_number = order_data['table_number']
        order.number_of_people = order_data['number_of_people']
        session.commit()
    return jsonify({'message': 'Order updated successfully'}), 200

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    with db.session as session:
        order = session.query(Order).get(order_id)
        session.delete(order)
        session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200

# OrderItem routes
@app.route('/orderitems', methods=['GET'])
def get_order_items():
    with db.session as session:
        order_items = session.query(OrderItem).all()
    return jsonify([item.serialize() for item in order_items]), 200

@app.route('/orderitems', methods=['POST'])
def create_order_item():
    order_item_data = request.json
    order_item = OrderItem(
        order_id=order_item_data['order_id'],
        item_type=order_item_data['item_type'],
        item_id=order_item_data['item_id'],
        quantity=order_item_data['quantity']
    )
    with db.session as session:
        session.add(order_item)
        session.commit()
    return jsonify({'message': 'Order item created successfully'}), 201

@app.route('/orderitems/<int:order_item_id>', methods=['PUT'])
def update_order_item(order_item_id):
    order_item_data = request.json
    with db.session as session:
        order_item = session.query(OrderItem).get(order_item_id)
        order_item.order_id = order_item_data['order_id']
        order_item.item_type = order_item_data['item_type']
        order_item.item_id = order_item_data['item_id']
        order_item.quantity = order_item_data['quantity']
        session.commit()
    return jsonify({'message': 'Order item updated successfully'}), 200

@app.route('/orderitems/<int:order_item_id>', methods=['DELETE'])
def delete_order_item(order_item_id):
    with db.session as session:
        order_item = session.query(OrderItem).get(order_item_id)
        session.delete(order_item)
        session.commit()
    return jsonify({'message': 'Order item deleted successfully'}), 200

# FoodItem routes
@app.route('/fooditems', methods=['GET'])
def get_food_items():
    with db.session as session:
        food_items = session.query(FoodItem).all()
    return jsonify([item.serialize() for item in food_items]), 200

@app.route('/fooditems', methods=['POST'])
def create_food_item():
    food_item_data = request.json
    food_item = FoodItem(
        name=food_item_data['name'],
        price=food_item_data['price'],
        quantity=food_item_data['quantity'],
        status=food_item_data['status'],
    )
    with db.session as session:
        session.add(food_item)
        session.commit()
    return jsonify({'message': 'FoodItem created successfully'}), 201

@app.route('/fooditems/<int:food_item_id>', methods=['PUT'])
def update_food_item(food_item_id):
    food_item_data = request.json
    with db.session as session:
        food_item = session.query(FoodItem).get(food_item_id)
        food_item.name = food_item_data['name']
        food_item.price = food_item_data['price']
        food_item.quantity = food_item_data['quantity']
        food_item.status = food_item_data['status']
        session.commit()
    return jsonify({'message': 'FoodItem updated successfully'}), 200

@app.route('/fooditems/<int:food_item_id>', methods=['DELETE'])
def delete_food_item(food_item_id):
    with db.session as session:
        food_item = session.query(FoodItem).get(food_item_id)
        session.delete(food_item)
        session.commit()
    return jsonify({'message': 'FoodItem deleted successfully'}), 200

# StoreItem routes
@app.route('/storeitems', methods=['GET'])
def get_store_items():
    with db.session as session:
        store_items = session.query(StoreItem).all()
    return jsonify([item.serialize() for item in store_items]), 200

@app.route('/storeitems', methods=['POST'])
def create_store_item():
    store_item_data = request.json
    store_item = StoreItem(
        name=store_item_data['name'],
        price=store_item_data['price'],
        quantity=store_item_data['quantity']
    )
    with db.session as session:
        session.add(store_item)
        session.commit()
    return jsonify({'message': 'Store item created successfully'}), 201

@app.route('/storeitems/<int:store_item_id>', methods=['PUT'])
def update_store_item(store_item_id):
    store_item_data = request.json
    with db.session as session:
        store_item = session.query(StoreItem).get(store_item_id)
        store_item.name = store_item_data['name']
        store_item.price = store_item_data['price']
        store_item.quantity = store_item_data['quantity']
        session.commit()
    return jsonify({'message': 'Store item updated successfully'}), 200

@app.route('/storeitems/<int:store_item_id>', methods=['DELETE'])
def delete_store_item(store_item_id):
    with db.session as session:
        store_item = session.query(StoreItem).get(store_item_id)
        session.delete(store_item)
        session.commit()
    return jsonify({'message': 'Store item deleted successfully'}), 200

# AquaticItem routes
@app.route('/aquaticitems', methods=['GET'])
def get_aquatic_items():
    with db.session as session:
        aquatic_items = session.query(AquaticItem).all()
    return jsonify([item.serialize() for item in aquatic_items]), 200

@app.route('/aquaticitems', methods=['POST'])
def create_aquatic_item():
    aquatic_item_data = request.json
    aquatic_item = AquaticItem(
        name=aquatic_item_data['name'],
        price=aquatic_item_data['price'],
        quantity=aquatic_item_data['quantity']
    )
    with db.session as session:
        session.add(aquatic_item)
        session.commit()
    return jsonify({'message': 'Aquatic item created successfully'}), 201

@app.route('/aquaticitems/<int:aquatic_item_id>', methods=['PUT'])
def update_aquatic_item(aquatic_item_id):
    aquatic_item_data = request.json
    with db.session as session:
        aquatic_item = session.query(AquaticItem).get(aquatic_item_id)
        aquatic_item.name = aquatic_item_data['name']
        aquatic_item.price = aquatic_item_data['price']
        aquatic_item.quantity = aquatic_item_data['quantity']
        session.commit()
    return jsonify({'message': 'Aquatic item updated successfully'}), 200

@app.route('/aquaticitems/<int:aquatic_item_id>', methods=['DELETE'])
def delete_aquatic_item(aquatic_item_id):
    with db.session as session:
        aquatic_item = session.query(AquaticItem).get(aquatic_item_id)
        session.delete(aquatic_item)
        session.commit()
    return jsonify({'message': 'Aquatic item deleted successfully'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
