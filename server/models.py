from setup import db, bcrypt, flash
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from datetime import datetime




# class User(db.Model, UserMixin):


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admin"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    contact = db.Column(db.String)
    address = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    products = db.relationship('Product', backref='admin', lazy=True)
    _password_hash = db.Column(db.String, nullable=False)

    @hybrid_property
    def password_hash(self):
        return{"message": "You can't view password hashes"}
    
    @password_hash.setter
    def password_hash(self, password):
        our_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = our_hash.decode('utf-8')

    def validate_password(self, password):
        is_valid = bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
        return is_valid

    def __repr__(self):
        return f"Admin('{self.name}', '{self.email}', '{self.id}')"
    


class User(db.Model):
    __tablename__ = "user"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    contact = db.Column(db.String)
    
    address = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    order = db.relationship('Order', backref='user', lazy=True)
    _password_hash = db.Column(db.String, nullable=False)
    @hybrid_property
    def password_hash(self):
        return{"message": "You can't view password hashes"}
    
    @password_hash.setter
    def password_hash(self, password):
        our_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = our_hash.decode('utf-8')

    def validate_password(self, password):
        is_valid = bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
        return is_valid

    def add_to_orders(self,product_id):
        item_to_add = Order(product_id=product_id, user_id=self.id)
        db.session.add(item_to_add)
        db.session.commit()
        flash('Your order has been made succesfully!', 'success')

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}', '{self.email}','{self.id}')"



class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'brand': self.brand,
            'image_url': self.image_url,
            'quantity': self.quantity,
            'admin_id': self.admin_id
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    review = db.Column(db.String(200))

    def __repr__(self):
        return f"Cart('Product id:{self.product_id}','id: {self.id}','User id:{self.user_id}'')"
    

# class Reviews(db.Model):
#     __tablename__ = "reviews"
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     comment = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f"Reviews('{self.product_id}', '{self.user_id}', '{self.rating}')"    

