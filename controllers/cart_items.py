from flask import request, jsonify
from config.db_config import db, CartItem

# ========================= CRUD OPERATIONS =========================

# 📌 1. Create a new cart item (POST)
def create_cart_item():
    try:
        data = request.json
        new_cart_item = CartItem(
            user_id=data["user_id"],
            product_id=data["product_id"],
            quantity=data["quantity"],
            price_details=data["price_details"],
            created_by=data.get("created_by", -1),
            last_modified_by=data.get("last_modified_by", -1),
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({"message": "Cart item created successfully", "cart_item_id": new_cart_item.cart_item_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating cart item: {str(e)}"}), 500

# 📌 2. Get all cart items for a user (GET)
def get_cart_items_by_user(user_id):
    try:
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({"message": "No cart items found for this user"}), 404
        
        cart_items_list = [
            {
                "cart_item_id": item.cart_item_id,
                "user_id": item.user_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_details": item.price_details,
                "created_date": item.created_date,
                "created_by": item.created_by,
                "last_modified_date": item.last_modified_date,
                "last_modified_by": item.last_modified_by
            } for item in cart_items
        ]
        return jsonify(cart_items_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching cart items: {str(e)}"}), 500

# 📌 3. Get a single cart item by ID (GET)
def get_cart_item(cart_item_id):
    try:
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({"message": "Cart item not found"}), 404
        
        return jsonify({
            "cart_item_id": cart_item.cart_item_id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "price_details": cart_item.price_details,
            "created_date": cart_item.created_date,
            "created_by": cart_item.created_by,
            "last_modified_date": cart_item.last_modified_date,
            "last_modified_by": cart_item.last_modified_by
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching cart item: {str(e)}"}), 500

# 📌 4. Update cart item by ID (PUT)
def update_cart_item(cart_item_id):
    try:
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({"message": "Cart item not found"}), 404
        
        data = request.json
        cart_item.quantity = data.get("quantity", cart_item.quantity)
        cart_item.price_details = data.get("price_details", cart_item.price_details)
        cart_item.last_modified_by = data.get("last_modified_by", cart_item.last_modified_by)

        db.session.commit()
        return jsonify({"message": "Cart item updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating cart item: {str(e)}"}), 500

# 📌 5. Delete cart item by ID (DELETE)
def delete_cart_item(cart_item_id):
    try:
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({"message": "Cart item not found"}), 404

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Cart item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting cart item: {str(e)}"}), 500


# 📌 6. Delete cart items by ID (POST)
def delete_cart_items():
    cartitems = request.json
    try:
        cart_item_ids = [p['cart_item_id'] for p in cartitems]

        if not cart_item_ids:
            return jsonify([]), 200
    
        cart_items = CartItem.query.filter(CartItem.cart_item_id.in_(cart_item_ids)).all()
        if not cart_items:
            return jsonify({"message": "Cart item not found"}), 404

        db.session.delete(cart_items)
        db.session.commit()
        return jsonify({"message": "Cart item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting cart item: {str(e)}"}), 500
