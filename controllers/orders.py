from flask import Flask, request, jsonify
from config.db_config import db, Order

# ========================= CRUD OPERATIONS =========================

# 📌 1. Create a new order (POST)
#@app.route("/orders", methods=["POST"])
def create_order():
    try:
        data = request.json
        new_order = Order(
            user_id=data["user_id"],
            final_price=data["final_price"],
            discount_price=data["discount_price"],
            payment_details=data.get("payment_details", "Cash"),
            created_by=data.get("created_by", -1),
            last_modified_by=data.get("last_modified_by", -1),
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order created successfully", "order_id": new_order.order_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating order: {str(e)}"}), 500

# 📌 2. Get all orders (GET)
#@app.route("/orders", methods=["GET"])
def get_all_orders():
    try:
        orders = Order.query.all()
        if not orders:
            return jsonify({"message": "No orders found"}), 404
        
        orders_list = [
            {
                "order_id": order.order_id,
                "user_id": order.user_id,
                "final_price": order.final_price,
                "discount_price": order.discount_price,
                "payment_details": order.payment_details,
                "created_date": order.created_date,
                "created_by": order.created_by,
                "last_modified_date": order.last_modified_date,
                "last_modified_by": order.last_modified_by
            } for order in orders
        ]
        return jsonify(orders_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching orders: {str(e)}"}), 500

# 📌 3. Get a single order by ID (GET)
#@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        
        return jsonify({
            "order_id": order.order_id,
            "user_id": order.user_id,
            "final_price": order.final_price,
            "discount_price": order.discount_price,
            "payment_details": order.payment_details,
            "created_date": order.created_date,
            "created_by": order.created_by,
            "last_modified_date": order.last_modified_date,
            "last_modified_by": order.last_modified_by
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching order: {str(e)}"}), 500

# 📌 4. Update order by ID (PUT)
#@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        
        data = request.json
        order.final_price = data.get("final_price", order.final_price)
        order.discount_price = data.get("discount_price", order.discount_price)
        order.payment_details = data.get("payment_details", order.payment_details)
        order.last_modified_by = data.get("last_modified_by", order.last_modified_by)

        db.session.commit()
        return jsonify({"message": "Order updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating order: {str(e)}"}), 500

# 📌 5. Delete order by ID (DELETE)
#@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404

        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting order: {str(e)}"}), 500

