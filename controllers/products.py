from flask import Flask, request, jsonify
from config.db_config import db, Product, CartItem

# ========================= CRUD OPERATIONS =========================

# 📌 1. Create a new product (POST)
#@app.route("/products", methods=["POST"])
def create_product():
    try:
        data = request.json
        new_product = Product(
            product_name=data["product_name"],
            category=data.get("category", ""),
            price=data["price"],
            available_quantity=data["available_quantity"],
            offer=data.get("offer"),
            shop_id=data["shop_id"],
            product_image=data.get("product_image"),
            created_by=data.get("created_by", -1),
            last_modified_by=data.get("last_modified_by", -1),
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully", "product_id": new_product.product_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating product: {str(e)}"}), 500

# 📌 2. Get all products (GET)
#@app.route("/products", methods=["GET"])
def get_all_products():
    try:
        products = Product.query.all()
        if not products:
            return jsonify({"message": "No products found"}), 404
        
        products_list = [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "category": product.category,
                "price": product.price,
                "available_quantity": product.available_quantity,
                "offer": product.offer,
                "shop_id": product.shop_id,
                "product_image": product.product_image,
                "created_date": product.created_date,
                "created_by": product.created_by,
                "last_modified_date": product.last_modified_date,
                "last_modified_by": product.last_modified_by
            } for product in products
        ]
        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching products: {str(e)}"}), 500

# 📌 3. Get a single product by ID (GET)
#@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        return jsonify({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "category": product.category,
            "price": product.price,
            "available_quantity": product.available_quantity,
            "offer": product.offer,
            "shop_id": product.shop_id,
            "product_image": product.product_image,
            "created_date": product.created_date,
            "created_by": product.created_by,
            "last_modified_date": product.last_modified_date,
            "last_modified_by": product.last_modified_by
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching product: {str(e)}"}), 500

def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        return jsonify({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "category": product.category,
            "price": product.price,
            "available_quantity": product.available_quantity,
            "offer": product.offer,
            "shop_id": product.shop_id,
            "product_image": product.product_image,
            "created_date": product.created_date,
            "created_by": product.created_by,
            "last_modified_date": product.last_modified_date,
            "last_modified_by": product.last_modified_by
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching product: {str(e)}"}), 500

# 📌 4. Update product by ID (PUT)
#@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        data = request.json
        product.product_name = data.get("product_name", product.product_name)
        product.category = data.get("category", product.category)
        product.price = data.get("price", product.price)
        product.available_quantity = data.get("available_quantity", product.available_quantity)
        product.offer = data.get("offer", product.offer)
        product.shop_id = data.get("shop_id", product.shop_id)
        product.product_image = data.get("product_image", product.product_image)
        product.last_modified_by = data.get("last_modified_by", product.last_modified_by)

        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating product: {str(e)}"}), 500

# 📌 5. Delete product by ID (DELETE)
#@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting product: {str(e)}"}), 500

# 📌 6. Fetch product by Shop ID (GET)
def get_product_by_shop_id(shop_id):
    try:
        products = Product.query.filter_by(shop_id=shop_id).all()
        products_list = [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "category": product.category,
                "price": product.price,
                "available_quantity": product.available_quantity,
                "offer": product.offer,
                "shop_id": product.shop_id,
                "product_image": product.product_image,
                "created_date": product.created_date,
                "created_by": product.created_by,
                "last_modified_date": product.last_modified_date,
                "last_modified_by": product.last_modified_by
            } for product in products
        ]
        
        if not products:
            return jsonify({"message": "No products added for this shop.."}), 404
        else: return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching product: {str(e)}"}), 500

# 📌 6. Fetch product by Shop ID (GET)
def get_user_Cart_products(user_id):
    try:
        # product_ids = db.session.query(CartItem.product_id).filter(CartItem.user_id == user_id).all()
        cartitems = [
            {"cart_item_id": c.cart_item_id, "product_id": c.product_id, "quantity": c.quantity}
            for c in CartItem.query.with_entities(CartItem.cart_item_id, CartItem.product_id, CartItem.quantity).filter_by(user_id=user_id).all()
        ]

        product_ids = [p['product_id'] for p in cartitems]

        if not product_ids:
            return jsonify([]), 200
    
        products = Product.query.filter(Product.product_id.in_(product_ids)).all()
        products_list = [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "category": product.category,
                "price": product.price,
                "available_quantity": product.available_quantity,
                "offer": product.offer,
                "shop_id": product.shop_id,
                "product_image": product.product_image,
                "created_date": product.created_date,
                "created_by": product.created_by,
                "last_modified_date": product.last_modified_date,
                "last_modified_by": product.last_modified_by,
                "cart_item_id": next((d['cart_item_id'] for d in cartitems if d["product_id"] == product.product_id), None),
                "quantity": next((d['quantity'] for d in cartitems if d["product_id"] == product.product_id), None)
            } for product in products
        ]
        
        if not products:
            return jsonify({"message": "No products added for this shop.."}), 404
        else: return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching product: {str(e)}"}), 500