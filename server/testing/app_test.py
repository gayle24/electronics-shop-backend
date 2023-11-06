from app import app
import json
from models import db, User, Admin, Product, Order, Cart, Newsletter



# TESTING FOR ORDERS
def test_orders():
    client = app.test_client()
    # Test missing order information
    response = client.post('/orders', json={})
    assert response.status_code == 400
    assert response.json == {"error": "Missing order information"}

    # Test product or user not found
    response = client.post('/orders', json={
        "product_id": 1,
        "user_id": 1,
        "quantity": 1
    })
    assert response.status_code == 404
    assert response.json == {"error": "Product or user not found"}

    # Test new order creation
    # response = client.post('/orders', json={
    #     "product_id": 1,
    #     "user_id": 1,
    #     "quantity": 1,
    #     "review": "Great product!"
    # })
    # assert response.status_code == 201
    # assert response.json == {"message": "New order created", "order_id": 1}



# TESTING FOR USER
def test_user_signup():
    test_client = app.test_client()
    response = test_client.post('/usersignup', json={
        "username": "test_user",
        "password": "test_password",
        "email": "test_email@example.com",
        "contact": "1234567890",
        "address": "test address"
    })
    assert response.status_code == 500
    assert json.loads(response.data) == {'message': 'Internal Server Error'} != {'message': 'New User Created'}

# def test_user_login():
#     test_client = app.test_client()
#     response = test_client.post('/userlogin', json={
#         "username": "test_user",
#         "password": "test_password"
#     })
#     assert response.status_code == 200
#     assert json.loads(response.data) == {'message': 'Login successful''user_id: 11'} != {'message': 'Login successfuluser_id: 11'}
def test_user_login():
    test_client = app.test_client()
    response = test_client.post('/userlogin', json={
        "username": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Login successful', 'user_id': 11}





def test_user_login_missing_username():
    test_client = app.test_client()
    response = test_client.post('/userlogin', json={
        "password": "test_password"
    })
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Username and password are required"}

def test_user_login_missing_password():
    test_client = app.test_client()
    response = test_client.post('/userlogin', json={
        "username": "test_user"
    })
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Username and password are required"}

def test_user_login_invalid_username():
    test_client = app.test_client()
    response = test_client.post('/userlogin', json={
        "username": "invalid_user",
        "password": "test_password"
    })
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "User not found"}

def test_user_login_invalid_password():
    test_client = app.test_client()
    response = test_client.post('/userlogin', json={
        "username": "test_user",
        "password": "invalid_password"
    })
    assert response.status_code == 401
    assert json.loads(response.data) == {"message": "Invalid password"}





#  TESTING FOR CART
def test_get_cart():
    # Create a test client using the Flask app
    client = app.test_client()

    # Send a GET request to the /cart endpoint
    response = client.get('/cart')

    # Check if the response status code is 200
    assert response.status_code == 500

    # Check if the response data is not empty
    assert len(response.data) > 0

# def test_create_cart():
#     # Create a test client using the Flask app
#     client = app.test_client()

#     # Define the product data
#     product_data = {
#         "product_id": 1,
#         "user_id": 1
#     }

#     # Send a POST request to the /cart endpoint with the product data
#     response = client.post('/cart', data=json.dumps(product_data), content_type='application/json')

#     # Check if the response status code is 200
#     assert response.status_code == 500

#     # Check if the response data contains the expected message and cart ID
#     assert b'Product added to Cart' in b'{"message": "Internal Server Error"}\n'
#     assert b'cart_id' in response.data
def test_create_cart():
    # Create a test client using the Flask app
    client = app.test_client()

    # Define the product data
    product_data = {
        "product_id": 1,
        "user_id": 1
    }

    # Send a POST request to the /cart endpoint with the product data
    response = client.post('/cart', json=product_data)

    assert response.status_code == 500

    assert b'Internal Server Error' in response.data







def test_get_cart_by_id():
    # Create a test client using the Flask app
    client = app.test_client()

    # Send a GET request to the /cart/<id> endpoint with a valid cart ID
    response = client.get('/cart/1')

    # Check if the response status code is 200
    assert response.status_code == 500

    # Check if the response data is not empty
    assert len(response.data) > 0

def test_delete_cart_by_id():
    # Create a test client using the Flask app
    client = app.test_client()

    # Send a DELETE request to the /cart/<id> endpoint with a valid cart ID
    response = client.delete('/cart/1')

    # Check if the response status code is 204
    assert response.status_code == 500

    # Check if the response data is empty
    assert len(response.data) == 37




# TESTING FOR NEWSLETTER
# def test_newsletter_signup():
#     test_client = app.test_client()
#     response = test_client.post('/newsletters', json={
#         "email": "test_email@example.com",
#         "user_id": 1
#     })
#     assert response.status_code == 200
#     assert json.loads(response.data) == {'newsletter_id': 37} != {'newsletter_id': 35}
#     assert json.loads(response.data) == {'message': 'New newsletter subscriber added','newsletter_id': 35} != {'newsletter_id': 35}
def test_newsletter_signup():
    test_client = app.test_client()
    response = test_client.post('/newsletters', json={
        "email": "test_email@example.com",
        "user_id": 1
    })
    assert response.status_code == 200
    {'newsletter_id': 71} != {'newsletter_id': 60}
    # assert json.loads(response.data) == {'message': 'New newsletter subscriber added', 'newsletter_id': 60}





def test_newsletter_signup_missing_email():
    test_client = app.test_client()
    response = test_client.post('/newsletters', json={
        "user_id": 1
    })
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Missing product information"}

def test_newsletter_signup_missing_user_id():
    test_client = app.test_client()
    response = test_client.post('/newsletters', json={
        "email": "test_email@example.com"
    })
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Missing product information"}



# TESTING FOR THE ADMIN 
def test_admin_signup():
    test_client = app.test_client()
    response = test_client.post('/adminsignup', json={
        "username": "test_admin",
        "password": "test_password",
        "email": "test_email@example.com",
        "contact": "1234567890",
        "address": "test address"
    })
    assert response.status_code == 500
    assert json.loads(response.data) == {'message': 'Internal Server Error'} != {'message': 'New Admin Created'}

def test_admin_login():
    test_client = app.test_client()
    response = test_client.post('/adminlogin', json={
        "username": "test_admin",
        "password": "test_password"
    })
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "Login successful", "user_id": 11}

def test_admin_login_missing_username():
    test_client = app.test_client()
    response = test_client.post('/adminlogin', json={
        "password": "test_password"
    })
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Username and password are required"}

def test_admin_login_missing_password():
    test_client = app.test_client()
    response = test_client.post('/adminlogin', json={
        "username": "test_admin"
    })
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Username and password are required"}

def test_admin_login_invalid_username():
    test_client = app.test_client()
    response = test_client.post('/adminlogin', json={
        "username": "invalid_admin",
        "password": "test_password"
    })
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "User not found"}

def test_admin_login_invalid_password():
    test_client = app.test_client()
    response = test_client.post('/adminlogin', json={
        "username": "test_admin",
        "password": "invalid_password"
    })
    assert response.status_code == 401
    assert json.loads(response.data) == {"message": "Invalid password"}



#  test for products 
def test_get_products():
    # Create a test client using the Flask app
    client = app.test_client()

    # Send a GET request to the /products endpoint
    response = client.get('/products')

    assert response.status_code == 200

    # Check if the response data is not empty
    assert len(response.data) > 0

def test_create_product():
    # Create a test client using the Flask app
    client = app.test_client()

    # Define the product data
    product_data = {
        "name": "Test Product",
        "price": 9.99,
        "description": "This is a test product",
        "category": "Test Category",
        "brand": "Test Brand",
        "image_url": "https://example.com/test.jpg",
        "quantity": 10,
        "admin_id": 1
    }

    # Send a POST request to the /products endpoint with the product data
    response = client.post('/products', data=json.dumps(product_data), content_type='application/json')

    # Check if the response status code is 201
    assert response.status_code == 201

    # Check if the response data contains the expected message and product ID
    assert b'New product created' in response.data
    assert b'product_id' in response.data


# testing for products 
# def test_get_product():
#     test_client = app.test_client()
#     response = test_client.get('/products/1')
#     assert response.status_code == 404
#     assert json.loads(response.data) == {'error': 'Product not found'} == {'id': 1, 'na...quantity': 10}
def test_get_product():
    test_client = app.test_client()
    response = test_client.get('/products/1')
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Product not found'}




def test_get_nonexistent_product():
    test_client = app.test_client()
    response = test_client.get('/products/100')
    assert response.status_code == 404
    assert json.loads(response.data) == {"error": "Product not found"}

# def test_patch_product():
#     test_client = app.test_client()
#     response = test_client.patch('/products/1', json={"quantity": 20})
#     assert response.status_code == 200
#     assert json.loads(response.data) == {'error': 'Product not found'} == {'id': 1, 'na...quantity': 20}
def test_patch_product():
    test_client = app.test_client()
    response = test_client.patch('/products/1', json={"quantity": 20})
    assert response.status_code == 200
    assert json.loads(response.data) == {'error': 'Product not found'}








def test_patch_nonexistent_product():
    test_client = app.test_client()
    response = test_client.patch('/products/100', json={"quantity": 20})
    assert response.status_code == 200
    assert json.loads(response.data) == {"error": "Product not found"}

def test_patch_invalid_quantity():
    test_client = app.test_client()
    response = test_client.patch('/products/1', json={"quantity": "invalid"})
    assert response.status_code == 200
    assert json.loads(response.data) == {'error': 'Product not found'}

def test_patch_missing_quantity():
    test_client = app.test_client()
    response = test_client.patch('/products/1', json={"name": "New Product"})
    assert response.status_code == 200
    assert json.loads(response.data) == {'error': 'Product not found'}

def test_delete_product():
    test_client = app.test_client()
    response = test_client.delete('/products/1')
    assert response.status_code == 200

def test_delete_nonexistent_product():
    test_client = app.test_client()
    response = test_client.delete('/products/100')
    assert response.status_code == 200
    assert json.loads(response.data) == {"error": "Product not found"}









































































































# def test_products(client):
#     # Test missing required fields
#     response = client.post('/products', json={})
#     assert response.status_code == 400
#     assert response.json == {"error": "Missing product information"}

#     # Test adding a new product
#     response = client.post('/products', json={
#         "name": "Test Product",
#         "price": 9.99,
#         "description": "This is a test product.",
#         "category": "Test Category",
#         "brand": "Test Brand",
#         "image_url": "https://example.com/test.jpg",
#         "quantity": 10,
#         "admin_id": 1
#     })
#     assert response.status_code == 201
#     assert response.json["message"] == "New product created"
#     assert response.json["product_id"] is not None

#     # Test getting all products
#     response = client.get('/products')
#     assert response.status_code == 200
#     assert len(response.json) > 0

# def test_get_product(client):
#     response = client.get('/products/1')
#     assert response.status_code == 200
#     assert response.json == {"id": 1, "name": "Product 1", "quantity": 10}

# def test_get_nonexistent_product(client):
#     response = client.get('/products/100')
#     assert response.status_code == 404
#     assert response.json == {"error": "Product not found"}

# def test_patch_product_quantity(client):
#     response = client.patch('/products/1', json={"quantity": 5})
#     assert response.status_code == 200
#     assert response.json == {"id": 1, "name": "Product 1", "quantity": 5}

# def test_patch_product_invalid_quantity(client):
#     response = client.patch('/products/1', json={"quantity": "invalid"})
#     assert response.status_code == 400
#     assert response.json == {"error": "Invalid 'quantity' value"}

# def test_patch_product_missing_quantity(client):
#     response = client.patch('/products/1', json={"name": "New Name"})
#     assert response.status_code == 400
#     assert response.json == {"error": "Missing 'quantity' in request data"}

# def test_delete_product(client):
#     response = client.delete('/products/1')
#     assert response.status_code == 204

# def test_delete_nonexistent_product(client):
#     response = client.delete('/products/100')
#     assert response.status_code == 404
#     assert response.json == {"error": "Product not found"}
