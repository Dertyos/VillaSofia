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
from models import db, User
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


#Orders    

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Get the order with the specified ID from the database.
    with db.session as session:
        order = session.query(Order).get(order_id)

    # Delete the order from the database.
    session.delete(order)
    session.commit()

    # Return a success message.
    return jsonify({'message': 'Order deleted successfully'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
