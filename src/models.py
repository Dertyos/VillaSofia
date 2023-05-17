from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    role = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date)
    user_name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "date_of_birth": self.date_of_birth,
            "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }

class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user_name = db.Column(db.String(120))
    change_type = db.Column(db.String(120))
    change_data = db.Column(db.Text)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer)
    number_of_people = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    items = db.relationship('OrderItem', backref='order', lazy=True)  # new field

    def __repr__(self):
        return '<Order %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "table_number": self.table_number,
            "number_of_people": self.number_of_people,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "items": [item.serialize() for item in self.items]
        }


class OrderItem(db.Model):  # new model
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer)
    item_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "quantity": self.quantity,
        }

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(120))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<FoodItem %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class StoreItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<StoreItem %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class AquaticItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<AquaticItem %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
