
from setup import app, Resource, api, db
from flask import make_response, jsonify, request
from models import User, Admin, Product, Order, Cart, Newsletter
from flask_cors import CORS
import sys

@app.route('/')
def index():
    return {"message": "electropulse backend page"}


CORS(app, resources = {r"/usersignup": {"origins": "http://localhost:5173"}})
class UserSignup(Resource):
    def post(self):
        userData = request.get_json()
        name = userData['username']
        password = userData['password']
        email = userData['email']
        contact = userData['contact']
        address = userData['address']

        new_user = User(name=name, email=email, contact=contact, address=address)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        response_data = {"message": "New User Created"}

        return response_data, 201
api.add_resource(UserSignup, '/usersignup')


CORS(app, resources = {r"/userlogin": {"origins": "http://localhost:5173"}})
class Userlogin(Resource):
    def post(self):
        login_data = request.get_json()
        name = login_data.get('username')
        password = login_data.get('password')

        if not name or not password:
            return {"message": "Username and password are required"}, 400
        
        user = User.query.filter_by(name=name).first()
        if not user:
            return {"message": "User not found"}, 404
        
        if not user.validate_password(password):
            return {"message": "Invalid password"}, 401
        
        response_data = {
            "message": "Login successful",
            "user_id": user.id
        }

        return response_data
api.add_resource(Userlogin, '/userlogin')

class Products(Resource):
    def get(self):
        print(sys.getrecursionlimit())
        products = Product.query.all()
        response_dict_list = []
        for item in products:
            response_dict = item.to_dict()
            response_dict_list.append(response_dict)

        resp = make_response(
            jsonify(response_dict_list), 
            200
        )
        return resp
    
    def post(self):
        product_data = request.get_json()
        name = product_data.get('name')
        price = product_data.get('price')
        description = product_data.get('description')
        category = product_data.get('category')
        brand = product_data.get('brand')
        image_url = product_data.get('image_url')
        quantity = product_data.get('quantity')
        admin_id = product_data.get('admin_id')

        if not name or not price or not description or not category or not quantity or not admin_id:
            return {"error": "Missing product information"}, 400

        new_product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            brand=brand,
            image_url=image_url,
            quantity=quantity,
            admin_id=admin_id
        )

        db.session.add(new_product)
        db.session.commit()

        response_data = {"message": "New product created", "product_id": new_product.id}

        return response_data, 201
api.add_resource(Products, '/products')

class ProductsByID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            response_dict = product.to_dict()
            status_code = 200
        else:
            response_dict = {"error": "Product not found"}
            status_code = 404

        resp = make_response(
            jsonify(response_dict),
            status_code
        )
        return resp
    
    def patch(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            return {"error": "Product not found"}
        data = request.get_json()

        if 'quantity' in data:
            try:
                product.quantity = int(data['quantity'])
                db.session.commit()
                return product.to_dict(), 200
            except ValueError:
                return {"error": "Invalid 'quantity' value"}, 400
        else:
            return {"error": "Missing 'quantity' in request data"}, 400
        

    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            return {"error": "Product not found"}
        
        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted successfully"}, 204

api.add_resource(ProductsByID, '/products/<int:id>')

class Cart(Resource):
    def get(self):
        carts = Cart.query.all()
        response_dict_list = []
        for item in carts:
            response_dict = item.to_dict()
            response_dict_list.append(response_dict)

        resp = make_response(
            jsonify(response_dict_list), 
            200
        )
        return resp
     
    def post(self):
        product_data = request.get_json()
        product_id = product_data.get('product_id')
        user_id= product_data.get('user_id')

        if not product_id or not user_id :
            return {"error": "Missing product information"}, 400

        new_product = Cart(
            user_id=user_id,
            product_id=product_id
        )

        db.session.add(new_product)
        db.session.commit()

        response_data = {"message": "Product added to Cart", "cart_id": new_product.id}
        return response_data
api.add_resource(Cart, '/cart')
    
class CartByID(Resource):
    def get(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            response_dict = cart.to_dict()
            status_code = 200
        else:
          response_dict = {"error": "Film not found"}
          status_code = 200
        response = make_response(
                jsonify(response_dict),
                200
            )
        return response

    def delete(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if not cart:
            return {"error": "Product not found"}
        
        db.session.delete(cart)
        db.session.commit()

        return {"message": "Product deleted successfully"}, 204

api.add_resource(CartByID, '/cart/<int:id>')

class Orders(Resource):
    def post(self):
        order_data = request.get_json()
        product_id = order_data.get('product_id')
        user_id = order_data.get('user_id')
        quantity = order_data.get('quantity')
        review = order_data.get('review')

        if not product_id or not user_id or not quantity:
            return {"error": "Missing order information"}, 400

        # Check if the provided product and user IDs exist
        product = Product.query.get(product_id)
        user = User.query.get(user_id)

        if not product or not user:
            return {"error": "Product or user not found"}, 404

        # Create a new Order instance and set its attributes
        new_order = Order(
            product_id=product_id,
            user_id=user_id,
            quantity=quantity,
            review=review
        )

        db.session.add(new_order)
        db.session.commit()

        response_data = {"message": "New order created", "order_id": new_order.id}

        return response_data, 201

api.add_resource(Orders, '/orders')

class Newsletters(Resource):
    def post(self):
        product_data = request.get_json()
        email = product_data.get('email')
        user_id= product_data.get('user_id')

        if not email or not user_id :
            return {"error": "Missing product information"}, 400

        new_subscriber = Newsletter(
            user_id=user_id,
            email=email
        )

        db.session.add(new_subscriber)
        db.session.commit()

        response_data = {"message": "New newsletter subscriber added", "newsletter_id": new_subscriber.id}
        return response_data
api.add_resource(Newsletters, '/newsletters')        

class ClientAddressUpdate(Resource):
    def patch(self, id):
        new_address = request.get_json().get('address')

        if not new_address:
            return {"error": "Missing address information"}, 400

        user = User.query.get(id)

        if not user:
            return {"error": "User not found"}, 404

        user.address = new_address
        db.session.commit()

        response_data = {"message": "Client's address updated"}

        return response_data, 200

api.add_resource(ClientAddressUpdate, '/address/<int:user_id>')


class AdminSignup(Resource):
    def post(self):
        userData = request.get_json()
        name = userData['username']
        password = userData['password']
        email = userData['email']
        contact = userData['contact']
        address = userData['address']

        new_admin = Admin(name=name, email=email, contact=contact, address=address)
        new_admin.password_hash = password

        db.session.add(new_admin)
        db.session.commit()

        response_data = {"message": "New Admin Created"}

        return response_data, 201
api.add_resource(AdminSignup, '/adminsignup')

class Adminlogin(Resource):
    def post(self):
        login_data = request.get_json()
        name = login_data.get('username')
        password = login_data.get('password')

        if not name or not password:
            return {"message": "Username and password are required"}, 400
        
        user = Admin.query.filter_by(name=name).first()
        if not user:
            return {"message": "User not found"}, 404
        
        if not user.validate_password(password):
            return {"message": "Invalid password"}, 401
        
        response_data = {
            "message": "Login successful",
            "user_id": user.id
        }

        return response_data
api.add_resource(Adminlogin, '/adminlogin')



if __name__ == '__main__':
    app.run(port=5555, debug=True, host='0.0.0.0')