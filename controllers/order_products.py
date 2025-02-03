from flask import Flask, request, jsonify
from config.db_config import db, OrderProduct

# ========================= CRUD OPERATIONS =========================

# 📌 1. Create a new order product (POST)
#@app.route("/order_products", methods=["POST"])
def create_order_product():
    try:
        data = request.json
        for d in data:
            new_order_product = OrderProduct(
                order_id=d["order_id"],
                product_id=d["product_id"],
                product_price_details=d.get("product_price_details", None),
                quantity=d["quantity"],
                created_by=d.get("created_by", -1),
                last_modified_by=d.get("last_modified_by", -1),
            )
            db.session.add(new_order_product)
        db.session.commit()
        return jsonify({"message": "Order product created successfully", "order_product_id": new_order_product.order_product_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating order product: {str(e)}"}), 500

# 📌 2. Get all order products (GET)
#@app.route("/order_products", methods=["GET"])
def get_all_order_products():
    try:
        order_products = OrderProduct.query.all()
        if not order_products:
            return jsonify({"message": "No order products found"}), 404
        
        order_products_list = [
            {
                "order_product_id": order_product.order_product_id,
                "order_id": order_product.order_id,
                "product_id": order_product.product_id,
                "product_price_details": order_product.product_price_details,
                "quantity": order_product.quantity,
                "created_date": order_product.created_date,
                "created_by": order_product.created_by,
                "last_modified_date": order_product.last_modified_date,
                "last_modified_by": order_product.last_modified_by
            } for order_product in order_products
        ]
        return jsonify(order_products_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching order products: {str(e)}"}), 500

# 📌 3. Get a single order product by ID (GET)
#@app.route("/order_products/<int:order_product_id>", methods=["GET"])
def get_order_product(order_product_id):
    try:
        order_product = OrderProduct.query.get(order_product_id)
        if not order_product:
            return jsonify({"message": "Order product not found"}), 404
        
        return jsonify({
            "order_product_id": order_product.order_product_id,
            "order_id": order_product.order_id,
            "product_id": order_product.product_id,
            "product_price_details": order_product.product_price_details,
            "quantity": order_product.quantity,
            "created_date": order_product.created_date,
            "created_by": order_product.created_by,
            "last_modified_date": order_product.last_modified_date,
            "last_modified_by": order_product.last_modified_by
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching order product: {str(e)}"}), 500

# 📌 4. Update order product by ID (PUT)
#@app.route("/order_products/<int:order_product_id>", methods=["PUT"])
def update_order_product(order_product_id):
    try:
        order_product = OrderProduct.query.get(order_product_id)
        if not order_product:
            return jsonify({"message": "Order product not found"}), 404
        
        data = request.json
        order_product.product_price_details = data.get("product_price_details", order_product.product_price_details)
        order_product.quantity = data.get("quantity", order_product.quantity)
        order_product.last_modified_by = data.get("last_modified_by", order_product.last_modified_by)

        db.session.commit()
        return jsonify({"message": "Order product updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating order product: {str(e)}"}), 500

# 📌 5. Delete order product by ID (DELETE)
#@app.route("/order_products/<int:order_product_id>", methods=["DELETE"])
def delete_order_product(order_product_id):
    try:
        order_product = OrderProduct.query.get(order_product_id)
        if not order_product:
            return jsonify({"message": "Order product not found"}), 404

        db.session.delete(order_product)
        db.session.commit()
        return jsonify({"message": "Order product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting order product: {str(e)}"}), 500

