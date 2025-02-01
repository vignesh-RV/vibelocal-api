from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app (for database setup)
app = Flask(__name__)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize database
db = SQLAlchemy(app)

# Define User Model
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    mobile_number = db.Column(db.BigInteger, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_image = db.Column(db.Text)
    created_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, nullable=False, default=-1)
    last_modified_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )
    last_modified_by = db.Column(db.Integer, nullable=False, default=-1)
    user_type = db.Column(db.String(100), nullable=False, default="BUYER")


# CartItem model
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    cart_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_details = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=-1)
    last_modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    last_modified_by = db.Column(db.Integer, nullable=False, default=-1)
    
    # Relationships
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')




# Product model
class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=False, default=0)
    available_quantity = db.Column(db.Integer, nullable=False, default=0)
    offer = db.Column(db.Integer, nullable=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False)
    product_image = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=-1)
    last_modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    last_modified_by = db.Column(db.Integer, nullable=False, default=-1)

    # Relationships
    shop = db.relationship('Shop', backref='products')



# Shop model
class Shop(db.Model):
    __tablename__ = 'shops'

    shop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(100), nullable=False, unique=True)
    shop_logo = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    offer = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(500), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=-1)
    last_modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    last_modified_by = db.Column(db.Integer, nullable=False, default=-1)




# Order model
class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, default=-1)
    final_price = db.Column(db.BigInteger, nullable=False, default=0)
    discount_price = db.Column(db.BigInteger, nullable=False, default=0)
    payment_details = db.Column(db.String(100), nullable=False, default='Cash')
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=-1)
    last_modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    last_modified_by = db.Column(db.Integer, nullable=False, default=-1)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))



# OrderProduct model
class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    order_product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    product_price_details = db.Column(db.String(500), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=-1)
    last_modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    last_modified_by = db.Column(db.Integer, nullable=False, default=-1)

    order = db.relationship('Order', backref=db.backref('order_products', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_products', lazy=True))


# Create tables (Only needed for first-time setup)
with app.app_context():
    db.create_all()
